# coding=gbk
# hoshino�����Ķ˿���ip
PORT = 6660
HOST = '127.0.0.1'  # ���ز���ʹ�ô������ã�QQ�ͻ��˺�bot��������ͬһ̨�������
# HOST = '0.0.0.0'      # ���Ź�������ʹ�ô������ã�����ȫ��

DEBUG = False  # ����ģʽ

WHITE_LIST = []
SUPERUSERS = [851404658]  # ��д�����û���QQ�ţ��������ð�Ƕ���","����
GUILDADMIN = []
NICKNAME = ('����', 'bot')  # �����˵��ǳơ������ǳƵ�ͬ��@bot������Ԫ�����ö���ǳ�

COMMAND_START = {''}  # ����ǰ׺�����ַ���ƥ���κ���Ϣ��
COMMAND_SEP = set()  # ����ָ�����hoshino����Ҫ�����ԣ�����Ϊset()���ɣ�

# ����ͼƬ��Э��
# ��ѡ http, file, base64
# ��QQ�ͻ�����bot�˲���ͬһ̨�����ʱ������httpЭ��
RES_PROTOCOL = 'file'
# ��Դ���ļ��У���ɶ���д��windows��ע�ⷴб��ת��
RES_DIR = r'./res/'
# ʹ��httpЭ��ʱ����д��ԭ���ϸ�urlӦָ��RES_DIRĿ¼
RES_URL = 'http://127.0.0.1:5000/static/'

# ���õ�ģ��
# ���γ��Բ���ʱ���ȱ���Ĭ��
# ����������ģ�飬�������Ķ�����˵������������������
# �м�һ���Կ������
MODULES_ON = {
    'botmanage',
    'dice',
    'avatar_gif',
    'codeonline',
    'Paimonchat',
    'Genshin_Paimon',
    'myb_exchange'
}
