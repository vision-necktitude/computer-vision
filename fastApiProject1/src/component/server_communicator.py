import requests

class ServerCommunicator:
    def __init__(self, server_url):
        """
        :param server_url: 서버의 기본 URL
        """
        self.server_url = server_url

    """
    :param endpoint: 서버의 특정 엔드포인트
    :param data: 서버로 전송할 데이터
    """
    def send_data(self, endpoint, data):
        url = f"{self.server_url}/{endpoint}"
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            # 성공적으로 데이터를 전송했을 때의 로직
            # print(f"Successfully sent data to {url}")
            return response.json()  # 서버로부터의 응답을 반환할 수 있습니다.
        except requests.RequestException as e:
            # 요청 실패 처리
            # print(f"Failed to send data to {url}: {e}")
            return None

    def sendTechNeckCount(self, count):
        """
        HTTP POST 요청을 사용하여 서버에 tech neck 카운트를 전송합니다.
        """
        url = "서버/endpoint"
        data = {'count': count}
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            # 성공적으로 데이터를 전송했을 때의 로직
            print(f"Successfully sent tech neck count: {count}")
        except requests.RequestException as e:
            # 요청 실패 처리
            print(f"Failed to send tech neck count: {e}")