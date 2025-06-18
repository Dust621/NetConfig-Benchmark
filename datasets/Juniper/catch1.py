import os
import json
import shutil
from bs4 import BeautifulSoup
from urllib.parse import urljoin

KEYWORD_MAP = {
    '要求': 'requirements',
    '设备要求': 'requirements',
    '概述': 'overview',
    '拓扑学': 'topology',
    'CLI 快速配置': 'quick_cli',
    '分步过程': 'step_by_step',
    '结果': 'result',
    '配置': 'configuration',
    '程序': 'procedure'
}

def extract_text(elem):
    if elem:
        return ' '.join(elem.get_text(separator=' ', strip=True).split())
    return ''

def extract_steps(ol):
    steps = []
    if ol:
        for idx, li in enumerate(ol.find_all('li', recursive=False), 1):
            description = extract_text(li.find('p'))
            pre_tags = li.find_all('pre')
            code_lines = []
            for pre in pre_tags:
                lines = pre.get_text().splitlines()
                code_lines.extend([line for line in lines if line.strip() != ''])
            steps.append({
                "step": idx,
                "description": description,
                "code": code_lines
            })
    return steps

def extract_content(elements):
    contents = []
    seen = set()
    skip_keywords = ['content_copy', 'zoom_out_map', 'Show more']
    for elem in elements:
        text = extract_text(elem)
        if text and all(kw not in text for kw in skip_keywords) and text not in seen:
            seen.add(text)
            contents.append(text)
    return ' '.join(contents).strip()

def extract_user_inputs(soup):
    return [kbd.get_text(strip=True) for kbd in soup.find_all('kbd', class_='ph userinput')]

def extract_code_blocks(soup):
    codes = []
    for pre in soup.find_all('pre'):
        text = pre.get_text(strip=True)
        if text:
            codes.append(text)
    return codes

def extract_images(soup, output_img_dir, page_title, html_base_path):
    images = []
    img_tags = soup.find_all('img')
    for i, img in enumerate(img_tags):
        src = img.get('src')
        if src:
            ext = os.path.splitext(src)[-1].split('?')[0]
            filename = f"{page_title}_{i+1}{ext}"
            full_path = os.path.join(output_img_dir, filename)
            images.append(full_path.replace('output_json/', ''))
            local_path = os.path.join(html_base_path, src)
            if os.path.exists(local_path):
                shutil.copy(local_path, full_path)
    return images

def map_keyword(title):
    for key in KEYWORD_MAP:
        if key in title:
            return KEYWORD_MAP[key]
    return None


def build_nested_structure(tags, output_img_dir, page_title, html_base_path):
    stack = []
    root = []
    for tag in tags:
        if tag.name not in ['h3', 'h4', 'h5']:
            continue
        level = int(tag.name[1])
        title = extract_text(tag)
        keyword = map_keyword(title)
        if not keyword:
            continue
        section = {
            'title': title,
            'level': level
        }
        content_nodes = []
        sibling = tag.find_next_sibling()
        while sibling and (not sibling.name or not sibling.name.startswith('h')):
            content_nodes.append(sibling)
            sibling = sibling.find_next_sibling()
        temp_html = ''.join(str(e) for e in content_nodes)
        temp_soup = BeautifulSoup(temp_html, 'html.parser')

        def should_extract_content(level, keyword):
            if level == 3 and keyword != 'configuration':
                return True
            if level == 4 and keyword == 'topology':
                return True
            return False
        extract_content_flag = should_extract_content(level, keyword)
        if level < 4:
            # 对于 h3 和 h4，只保留标题用于结构分级，不提取代码
            content = extract_content(temp_soup.find_all(['p', 'div']))
            if content:
                section['content'] = content

        else:
            if keyword == 'result':
                code_blocks = [pre.get_text(strip=True) for pre in temp_soup.find_all('pre')]
                for pre in temp_soup.find_all('pre'):
                    pre.decompose()
                content = extract_content(temp_soup.find_all(['p', 'div']))
                if content:
                    section['content'] = content
                if code_blocks:
                    section['code'] = code_blocks
            else:
                if keyword != 'step_by_step':
                    content = extract_content(temp_soup.find_all(['p', 'div']))
                    if content:
                        section['content'] = content

                if keyword == 'topology':
                    imgs = extract_images(temp_soup, output_img_dir, page_title, html_base_path)
                    if imgs:
                        section['images'] = imgs

                if keyword == 'quick_cli':
                    commands_by_device = {}
                    found_device = False
                    p_tags = temp_soup.find_all('p')

                    for p_tag in p_tags:
                        strong = p_tag.find('strong')
                        if not strong:
                            continue
                        device_name = extract_text(strong)
                        found_device = True

                        next_node = p_tag.find_next_sibling()
                        while next_node:
                            if next_node.name == 'pre':
                                break
                            elif next_node.find('pre'):
                                next_node = next_node.find('pre')
                                break
                            next_node = next_node.find_next_sibling()

                        if next_node and next_node.name == 'pre':
                            kbd_tags = next_node.find_all('kbd')
                            commands = [extract_text(kbd) for kbd in kbd_tags if extract_text(kbd)]
                            if commands:
                                commands_by_device[device_name] = '\n'.join(commands)

                    if found_device and commands_by_device:
                        section['commands_by_device'] = commands_by_device
                    else:
                        all_commands = []
                        for pre in temp_soup.find_all('pre'):
                            kbd_tags = pre.find_all('kbd')
                            cmds = [extract_text(kbd) for kbd in kbd_tags if extract_text(kbd)]
                            all_commands.extend(cmds)
                        if all_commands:
                            section['code'] = all_commands

                if keyword == 'step_by_step':
                    steps = extract_steps(temp_soup.find('ol'))
                    if steps:
                        section['step_by_step'] = steps

                user_inputs = extract_user_inputs(temp_soup)
                if user_inputs:
                    section['user_inputs'] = user_inputs

        while stack and stack[-1]['level'] >= level:
            stack.pop()
        if stack:
            stack[-1].setdefault('sections', []).append(section)
        else:
            root.append(section)
        stack.append(section)
    return root

# 新增：递归删除所有 sections 里的 user_inputs 字段
def remove_user_inputs_from_sections(sections):
    for section in sections:
        if 'user_inputs' in section:
            del section['user_inputs']
        if 'sections' in section:
            remove_user_inputs_from_sections(section['sections'])

def parse_h2_sections(soup, html_path, output_dir='output_json'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    img_output_dir = os.path.join(output_dir, 'images')
    os.makedirs(img_output_dir, exist_ok=True)
    html_base_path = os.path.dirname(html_path)
    h2_tags = soup.find_all('h2')
    print(f"[调试] 共找到 {len(h2_tags)} 个 h2 标签")
    count_saved = 0
    for idx, h2 in enumerate(h2_tags, 1):
        h2_title = extract_text(h2)
        print(f"[调试] h2 #{idx} 内容：{h2_title}")
        content_nodes = []
        next_node = h2.find_next_sibling()
        while next_node and next_node.name != 'h2':
            content_nodes.append(next_node)
            next_node = next_node.find_next_sibling()
        temp_html = ''.join(str(n) for n in content_nodes)
        temp_soup = BeautifulSoup(temp_html, 'html.parser')
        for a in temp_soup.find_all('a'):
            a.unwrap()
        sections = build_nested_structure(
            temp_soup.find_all(['h3', 'h4', 'h5']),
            img_output_dir,
            f"{idx}_{h2_title[:20].replace(' ', '_')}",
            html_base_path
        )
        if sections:
            remove_user_inputs_from_sections(sections)  # 这里删除 user_inputs
            section = {'title': h2_title, 'sections': sections}
            content = extract_content(temp_soup.find_all(['p', 'div'], recursive=False))
            if content:
                sentences = content.split('。')
                if len(sentences) > 1:
                    sentences = sentences[:-1]
                    content = '。'.join(sentences).strip()
                section['content'] = content
            safe_title = h2_title.replace(' ', '_').replace('/', '_')[:30]
            filename = os.path.join(output_dir, f"{idx}_{safe_title}.json")
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(section, f, ensure_ascii=False, indent=2)
            print(f"[已保存] {filename}")
            count_saved += 1
    print(f"[完成] 共保存 {count_saved} 个章节的 JSON 文件")

def main():
    html_path = "html/BGP 对等会话 _ Junos OS _ Juniper Networks.html"
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    print(f"[调试] HTML 文件已读取，长度：{len(html_content)}")
    soup = BeautifulSoup(html_content, 'html.parser')
    for a in soup.find_all('a'):
        a.unwrap()
    parse_h2_sections(soup, html_path, output_dir='output_json/BGP 对等会话')
    print("全部导出完成！")

if __name__ == '__main__':
    main()
