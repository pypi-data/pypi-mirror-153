class bong:
    """
    คลาส bong คือ
    ข้อมูลที่เกี่ยวข้องกับโบ้ง
    ประกอบด้วยชื่อโบ้ง
    ฟังก์ชั่นการกินเป็ด

    Example
    #===============================
    user = bong()
    user.show_name()
    user.eat()
    user.laugh()
    user.about()
    user.show_youtube()
    #===============================
    """

    def __init__(self):
        self.name = 'โบ้ง'
        self.page = 'https://www.youtube.com/channel/UCukIPSb0N6_vRVD_5VlzqQg'

    def show_name(self):
        print(f'สวัสดีฉันชื่อ{self.name}')

    def show_youtube(self):
        print(f'{self.page}')

    def eat(self):
        print(f'{self.name}กำลังกินเป็ด')
        print('แจ๊บๆๆๆๆๆๆๆๆๆๆๆๆๆๆ')
        print(f'{self.name}กินเป็ดจนหมด เหลือแต่ส่วนกระดูกคอให้เพื่อน')

    def about(self):
        text = """
        สวัสดีจ้าาาาาาา นี่โบ้งเอง เป็นนักกินเป็ด
        ชอบกินเป็ดตามโต๊ะจีนมากๆ และเหลือกระดูกคอไว้ให้เพื่อน
        """
        print(text)

    def laugh(self):
        print('ฮึๆๆๆๆๆๆๆๆๆๆๆๆๆๆๆๆๆๆๆๆ')

if __name__ == '__main__':
    user = bong()
    user.show_name()
    user.eat()
    user.about()
    user.show_youtube()
    user.laugh()