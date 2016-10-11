#! coding:utf-8

import requests
import logging
import logging.config
from bs4 import BeautifulSoup
from models import Job, session
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

SITE = "http://www.lagou.com/zhaopin/ceshi/?labelWords=label"
# SITE = "http://www.lagou.com/zhaopin/ceshi/1/?filterOption=3"

headers = {'content-type': 'application/json',
           'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
logging.config.fileConfig("logging.conf")
logger = logging.getLogger("spider")


def get_contents(soup):
    # 获取job info
    results = soup.select('.con_list_item')
    for result in results:
        content = result.attrs
        experience, education = result.select('.li_b_l')[0].get_text().replace(' ', '').strip().split('/')
        tag = result.select('.li_b_l')[1].get_text()
        positionname = content.get('data-positionname')
        positionid = content.get('data-positionid')
        companyid = content.get('data-positionid')
        salary = content.get('data-salary')
        s_salary, e_salary = split_salary(salary)
        company = content.get('data-company')
        area = result.select('.add')[0].find('em').get_text()
        job = Job(positionname=positionname, positionid=positionid, companyid=companyid, s_salary=s_salary,
                  e_salary=e_salary, company=company, status=0, area=area, experience=experience, education=education,
                  tag=tag)
        session.add(job)
        message = "{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}".format(
            positionname, positionid, companyid, s_salary, e_salary, company, area, experience, education, tag)
        logger.info(message)
    session.commit()


def split_salary(salary):
    if "-" in salary:
        a, b = salary.split('-')
        return [a[:-1], b[:-1]]
    elif u"以下" in salary:
        print '###' * 20 + salary + salary[:-7]
        return [0, str(salary)[:-3]]
    elif u"以上" in salary:
        print '###' * 20 + salary + salary[:-7]
        return [str(salary)[:-3], 999]


def get_max_num(soup):
    data = int(soup.select('.pager_container')[-1].find_all('a')[-2].get_text())
    logger.info("一共"+str(data)+"页")
    return data


def request_handler(url, head):
    html = requests.get(url=url, headers=head).text
    logger.info("请求的URL为：" + url)
    return html


def main():
    html = request_handler(SITE, headers)
    soup = BeautifulSoup(html, "lxml")
    max_num = get_max_num(soup)

    for page_number in range(1, max_num+1):
        print page_number
        real_url = "http://www.lagou.com/zhaopin/ceshi/" + str(page_number) + "/?filterOption=3"
        html = request_handler(real_url, headers)
        soup = BeautifulSoup(html, "lxml")
        get_contents(soup)


if __name__ == '__main__':
    main()