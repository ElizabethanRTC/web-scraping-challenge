import requests
import pymongo
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

def scrape_info():
    # executable_path = {"executable_path": "C:\Program Files\Google\Chrome\Application\Chrome.exe"}
    executable_path = {"executable_path": ChromeDriverManager().install()}
    browser = Browser("chrome", **executable_path, headless=False)

    #Website 1
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html = browser.html
    html

    news_soup = soup(html, 'html.parser')
    new_title = news_soup.find('div', class_= "content_title").text
    news_paragraph = news_soup.find('div', class_= "article_teaser_body").text
    url = 'https://spaceimages-mars.com'
    browser.visit(url)
    html = browser.html

    img_soup = soup(html, 'html.parser')
    img_soup
    img_endpoint = img_soup.find('img', class_='headerimage fade-in')['src']

    img_url = url + '/' + img_endpoint

    img_url

    #Website#2

    url = 'https://galaxyfacts-mars.com/'
    table = pd.read_html(url)[0].to_html()
    table

    #Website #3
    url = 'https://marshemispheres.com/cerberus.html'
    browser.visit(url)
    html = browser.html
    hemisphere_soup = soup(html, 'html.parser')
    hemisphere_soup

    base_url = 'https://marshemispheres.com/cerberus.html'
    hemisphere_img_end = hemisphere_soup.find_all('a', {'target': '_blank'})[2]['href']

    full_url = base_url + '/' + hemisphere_img_end

    base_url = 'https://marshemispheres.com'
    hemisphere_img_end = hemisphere_soup.find_all('a', {'target': '_blank'})[2]['href']

    base_url + '/' + hemisphere_img_end

    browser.visit(base_url)
    html = browser.html

    hemisphere_first_page_soup = soup(html, 'html.parser')
    hemisphere_first_page_soup

    found_result_list = hemisphere_first_page_soup.find_all('a', class_='itemLink product-item')

    list_of_hemisphere_pages = []

    for tag in found_result_list:
        if tag['href'] == '#': continue
        list_of_hemisphere_pages.append(base_url + '/' + tag['href'])
    final_urls = list(set(list_of_hemisphere_pages))
    final_urls


    list_of_hemisphere_dictionaries = []

    for url in final_urls:
        browser.visit(url)
        html = browser.html
        
        hemisphere_soup = soup(html, 'html.parser')
        hemisphere_img_end = hemisphere_soup.find_all('a', {'target': '_blank'})[2]['href']
        full_url = base_url + '/' + hemisphere_img_end
        
        hemisphere_title = hemisphere_soup.find('h2', class_='title').text
        
        dummy_dictionary = {'title': hemisphere_title, 'url': full_url}
        list_of_hemisphere_dictionaries.append(dummy_dictionary)
                        
    print(list_of_hemisphere_dictionaries)

    list_of_hemisphere_dictionaries


    browser.quit()


    mongo_dictionary = {
        'new_title': new_title,
        'new_paragraph': news_paragraph,
        'img_url': img_url,
        'table': table,
        'list_of_hemisphere_dictionaries': list_of_hemisphere_dictionaries

        
    }

    mongo_dictionary

    return mongo_dictionary