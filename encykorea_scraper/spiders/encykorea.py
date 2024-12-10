import scrapy
import json
from bs4 import BeautifulSoup


class EncykoreaSpider(scrapy.Spider):
    name = 'encykorea'

    # E0000001 ~ E0000100까지의 URL을 자동 생성
    start_urls = [f'https://encykorea.aks.ac.kr/Article/E{str(i).zfill(7)}' for i in range(1, 101)]

    def parse(self, response):
        try:

        # XPath로 지정된 위치에서 텍스트를 추출
            html_content = response.xpath(
                '''
                //div[@class="contents-detail-contents"]
                '''
            ).get()
            soup = BeautifulSoup(html_content, 'html.parser')

            for tag in soup.select('.contents-top.pdf-hidden-layer, .detail-section.section-toc, .star-rating-box, #cm_multimedia, button'):
                tag.decompose()
            
            extracted_text = soup.get_text(separator=" ", strip=True)

            # 데이터가 없는 경우 넘어가기
            if not extracted_text:
                self.logger.warning(f"No data found for URL: {response.url}")
                return
            

            # URL과 텍스트를 dictionary 형태로 저장
            data = {
                'url': response.url,
                'text': extracted_text
            }

            # JSON 파일로 저장하기 위해 반환
            yield data
            
        except Exception as e:
            # 에러 발생 시 로그 메시지 출력
            self.logger.warning(f"Error processing URL: {response.url} - {str(e)}")