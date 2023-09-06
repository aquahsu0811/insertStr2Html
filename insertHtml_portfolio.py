import os
import copy
from bs4 import BeautifulSoup


def getSplitStr(str):
    if '：' in str:  # 检查行中是否包含冒号
        parts = str.split('：', 1)  # 使用冒号拆分字符串，最多拆分成两部分
        if len(parts) == 2:  # 确保成功拆分成两部分
            value_after_colon = parts[1].strip()
            return value_after_colon


def addli(soup, html, imgURL, description, title ):

    # for line in lines:
    #     li_element = soup.new_tag('li', class_='mb-4')
    #     li_element.string = line
    #     ul_element.append(li_element)

    # 创建一个新的<li>元素
    new_li_element = soup.new_tag('li', attrs={'class': 'col my-4 wrapper'})

    # 创建并添加<a>元素
    new_a_element = soup.new_tag(
        'a', attrs={'class': 'card card-gallery'}, href=html, target='_blank')

    # 创建并添加<div>元素
    new_div_element = soup.new_tag('div', attrs={'class': 'card-img-body'})

    # 创建并添加<img>元素
    new_img_element = soup.new_tag(
        'img', alt=description, attrs={'class': 'card-img card-img-top image'}, src=imgURL)

    # 创建并添加<div>元素
    new_imageBg_element = soup.new_tag('div', attrs={'class': 'imageBg'})

    # 创建并添加<div>元素
    new_middle_element = soup.new_tag('div', attrs={'class': 'middle'})

    # 创建并添加<div>元素
    new_middle_title_element = soup.new_tag('div', attrs={'class': 'middle-title'})
    new_middle_title_element.string = title

    # 创建并添加<a>元素
    new_middle_readmore_element = soup.new_tag(
        'a',  attrs={'class': 'middle-readmore'}, href=html, target='_blank')
    new_middle_readmore_element.string = 'Read more'

    # 将所有元素按正确的层次添加到<li>元素中
    new_li_element.append(new_a_element)
    new_a_element.append(new_div_element)
    new_div_element.append(new_img_element)
    new_div_element.append(new_imageBg_element)
    new_li_element.append(new_middle_element)
    new_middle_element.append(new_middle_title_element)
    new_middle_element.append(new_middle_readmore_element)

    # 找到现有的<ul>元素
    existing_ul_element = soup.find(
        'ul', class_='row row-cols-1 row-cols-md-2 row-cols-lg-3')

    # 将新的<li>元素添加到现有的<ul>元素中
    existing_ul_element.append(new_li_element)


def addBImg(soup, folder_name, description, dist_src='assets/resized_photo/blog_2023-08-26/'):
    Bimg_item = soup.find(
        'div', class_='card-img-body work-card-img-body-main')

    new_img_element = soup.new_tag(
        'img', alt=description, attrs={'class': 'card-img card-img-top'}, src=dist_src+folder_name + '/首圖.jpg')
    Bimg_item.append(new_img_element)
    print(Bimg_item)


def addImg(soup, folder_name, img_src, description, dist_src='assets/resized_photo/blog_2023-08-26/'):
    water_fall_body = soup.find('div', class_='water-fall-body')
    new_water_fall_item = soup.new_tag(
        'div', attrs={'class': 'water-fall-item'})
    new_img_src = dist_src+folder_name+'/'+img_src
    new_img_element = soup.new_tag(
        'img', attrs={'class': 'card-img card-img-top'}, alt=description, src=new_img_src)
    new_water_fall_item.append(new_img_element)
    water_fall_body.append(new_water_fall_item)


def readHtml(templateFile):
    html_file_path = templateFile

    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # 使用Beautiful Soup解析HTML 並複製一份
    soupTemplate = BeautifulSoup(html_content, 'html.parser')
    soup = copy.copy(soupTemplate)

    return soup


def main(data_path, template):
    # 指定包含文件夹的目录

    soup = readHtml(template)
    for folder_name in os.listdir(data_path):
        folder_path = os.path.join(data_path, folder_name)

        if os.path.isdir(folder_path):
            print(f"子文件夹: {folder_name}")
            txt_files = [file for file in os.listdir(
                folder_path) if file.endswith('.txt')]

            first_line = 'test'
            last_line = 'test'
            for txt_file in txt_files:
                txt_path = os.path.join(folder_path, txt_file)
                try:
                    with open(txt_path, 'r', encoding='utf-8') as file:
                        first_line = file.readline().strip()
                        lines = file.readlines()
                        last_line = getSplitStr(lines[1])

                except FileNotFoundError:
                    print('not found')
                except Exception as e:
                    print(f"发生错误：{e}")
            #addBImg(soup, folder_name, folder_name)
            html_name = 'portfolio_' + folder_name + '.html'
            imgURL = 'assets/resized_photo/blog_2023-08-26/' + folder_name + '/首圖.jpg'
            description = folder_name
            title = first_line +'|' + last_line
            print('-------------------------')
            print(html_name)
            print(imgURL)
            print(description)
            print(title)
            addli(soup, html_name, imgURL, description, title )
    output_html_file = './output/portfolio_output.html'  # 指定要保存修改后的HTML的文件路径
    with open(output_html_file, 'w', encoding='utf-8') as file:
        file.write(str(soup))


if __name__ == "__main__":
    data_path = './data/data_20230826'
    main(data_path, 'portfolio.html')
