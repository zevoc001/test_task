from dotenv import load_dotenv
import requests, os


load_dotenv()

urls={
    'login': 'https://api.aut.finance/api/users/login',
    'get_transaction': 'https://api.aut.finance/api/transactions' 
}

def get_key(data: dict) -> str:
    '''
    data - Словарь данных авторизации.
    Словарь подается в виде {'login': 'value', 'password': 'value'} \n
    При успешной авторизации возвращает ключ сессии, иначе 0
    '''
    url = urls['login']
    response = requests.post(url, json=data)
    if response.status_code == 200:
        content = response.json()
        session_key = content['Authorization']
        return session_key
    else:
        raise

def get_transaction(api_key):
    url = urls['get_transaction']
    headers = {'Authorization': api_key}
    response = requests.get(url, headers=headers)
    transactions = response.json()
    return transactions


auth_data = {"email": os.getenv('LOGIN'), "password": os.getenv('PASSWORD')}
try:
    api_key = get_key(auth_data)
    response = get_transaction(api_key)
    if response:
        print(*response, sep='\n')
    else:
        print('Список транзакций пуст')
except:
    print('Ошибка авторизации')

