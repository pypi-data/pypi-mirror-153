from ugwayk.module import UgkSetDefault 

class UgkCalc(UgkSetDefault):
    def reset_all(self):
        # 계산기 초기화
        self.start_num = 0
    
    def plus(self, end_num, value_store = True):
        # 덧셈하는 구간
        retsult = self.start_num + end_num
        if value_store:
            # 결과값을 저장한 후로 연산을 이어가고 싶을 경우
            self.start_num = retsult
        return retsult
    
    def diff(self, end_num, value_store = True):
        retsult = self.start_num - end_num
        if value_store:
            # 결과값을 저장한 후로 연산을 이어가고 싶을 경우
            self.start_num = retsult
        return retsult
    
    def mult(self, end_num, value_store = True):
        retsult = self.start_num * end_num
        if value_store:
            # 결과값을 저장한 후로 연산을 이어가고 싶을 경우
            self.start_num = retsult
        return retsult
    
    def divide(self, end_num, value_store = True):
        if end_num == 0:
            raise ValueError("end_num cannot be 0")
        retsult = self.start_num / end_num
        if value_store:
            # 결과값을 저장한 후로 연산을 이어가고 싶을 경우
            self.start_num = retsult
        return retsult
    
    
    