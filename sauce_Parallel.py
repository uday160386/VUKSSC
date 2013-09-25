# -*- coding: iso-8859-1 -*-
import unittest, optparse, time, os
from selenium import webdriver
from array import *
import multiprocessing
import Queue
# Declaring the Suace list of browsers
SAUCEBROWSER = {
 'firefox': webdriver.DesiredCapabilities.FIREFOX,
 'ie': webdriver.DesiredCapabilities.INTERNETEXPLORER,
 'opera': webdriver.DesiredCapabilities.OPERA
}
# Declaring the Sauce OS environnment
SAUCEOS = {
 'xp': 'Windows 2003',
 'winxp': 'Windows 2003',
 'win2003': 'Windows 2003',
 'vista': 'Windows 2008',
 'win2008': 'Windows 2008',
 'linux': 'Linux'
}
class Selenium2OnSauce(unittest.TestCase):
    def setUp(self,s_browsers,s_userid,s_apikey,b_video,b_screenshot,s_testname):
      self.s_browsers = s_browsers
      self.s_userid = s_userid
      self.s_apikey = s_apikey
      self.s_testname = s_testname
      self.b_video = b_video
      self.b_screenshot = b_screenshot
      browser, version, os = self.s_browsers.split('-')
           
      desired_capabilities = SAUCEBROWSER[browser.lower()].copy()
      desired_capabilities['version'] = version if version.lower() != 'latest' else ''
      desired_capabilities['platform'] = SAUCEOS[os.lower()]
      desired_capabilities['name'] = self.s_testname
      desired_capabilities['record-video'] = self.b_video
      desired_capabilities['record-screenshots'] = self.b_screenshot
      self.driver = webdriver.Remote(desired_capabilities = desired_capabilities,command_executor = "http://{user}:{key}@{host}:{port}/wd/hub".format(user=self.s_userid, key=self.s_apikey, host="ondemand.saucelabs.com", port="80"))
      self.driver.implicitly_wait(30)
    def test_sauce(self):
      self.driver.get('http://saucelabs.com/test/guinea-pig')
      self.assertTrue("I am a page title - Sauce Labs" in self.driver.title);
      self.driver.find_element_by_id('comments').send_keys('Hello! I am some example comments. I should appear in the page after you submit the form')
      self.driver.find_element_by_id('submit').click()
      comments = self.driver.find_element_by_id('your_comments')
      self.assertTrue("Your comments: Hello! I am some example comments. I should appear in the page af  ter you submit the form" in comments.text)
      body = self.driver.find_element_by_xpath('//body')
      self.assertFalse('I am some other page content' in body.text)
      self.driver.find_elements_by_link_text('i am a link')[0].click()
      body = self.driver.find_element_by_xpath('//body')
      self.assertTrue('I am some other page content' in body.text)
    def tearDown(self):
      print "Link to your job: https://saucelabs.com/jobs/%s" % self.driver.session_id
      self.driver.quit()
def worker(l_browsers,s_suite,sauce_userid,sauce_apikey,sauce_video,sauce_screenshots,test_name):
  for test in s_suite:
             job_queue = multiprocessing.Queue()
             job_queue.put(test.setUp(l_browsers,sauce_userid,sauce_apikey,sauce_video,sauce_screenshots,test_name))
             job_queue.put(test.test_sauce())
             job_queue.put(test.tearDown())
             job_queue.put(unittest.TextTestRunner().run(s_suite))
             print
if __name__ == '__main__':
      parser = optparse.OptionParser(usage='usage: %prog [options]')
      parser.set_defaults(
        sauce_video=True,
        sauce_screenshots=True,
                         )
      parser.add_option('--sauce-user', action='store', dest='sauce_userid')
      parser.add_option('--sauce-key', action='store', dest='sauce_apikey')
      parser.add_option('--sauce-video', action='store_true', dest='sauce_video')
      parser.add_option('--sauce-screenshots', action='store_true', dest='sauce_screenshots')
      parser.add_option('--testName', action='store', dest='test_name')
      parser.add_option('--browser', action='store', dest='browser')
 
      o, args = parser.parse_args()
      arr_browser = []
      jobs = []
      arr_browser = o.browser.split(',') 
      suite = unittest.TestLoader().loadTestsFromTestCase(Selenium2OnSauce)
      for j in arr_browser:
          p = multiprocessing.Process(target=worker,args=(j,suite,o.sauce_userid,o.sauce_apikey,o.sauce_video,o.sauce_screenshots,o.test_name))
          jobs.append(p)
          p.start()
