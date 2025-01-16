class undergraduate:
    def __init__(self,name,age,scores):
        self.name=name
        self.age=age
        self.scores=scores
        self.scholarship = self.countscholarship()
    def countscholarship(self):
        if self.scores==5:
            return 6000
        else:
            return 4000
    def show_info(self):
        print(self.name,self.age)
    def show_scholarship(self):
        print(self.scholarship)
    def compare_scholarship(self,other):
        if self.scholarship>other.scholarship:
            print("more")
        else:
            print("less")

class graduate(undergraduate):
    def __init__(self,name,age,scores,work):
        super().__init__(name,age,scores)
        self.work=work
        self.countscholarship=self.countscholarship()
    def countscholarship(self):
        if self.scores == 5:
            return 8000
        else:
            return 6000


xiaom=undergraduate('xiaoming',15,3)
dam=graduate('dam',22,5,'science')
xiaom.compare_scholarship(dam)
