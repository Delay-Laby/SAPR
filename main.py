from GUI import Ui_MainWindow
import sys
from PyQt5.QtWidgets import QFileDialog,QTableWidgetItem
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import QPen
from PyQt5.QtCore import Qt
import numpy as np
import matplotlib.pyplot as plt

#Cохранение в фаил, отрисовка, процессор, процессор

class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.Rod_wiget.horizontalHeader().setSectionResizeMode(0,  QtWidgets.QHeaderView.ResizeToContents)
        self.ui.Rod_wiget.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.ui.Rod_wiget.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.ui.Rod_wiget.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        self.ui.Rod_wiget.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        self.ui.Node_wiget.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.ui.Node_wiget.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.ui.pushButton.clicked.connect(self.dobR)
        self.ui.pushButton_3.clicked.connect(self.dobN)
        self.ui.pushButton_5.clicked.connect(self.Del)
        self.ui.pushButton_4.clicked.connect(self.DelN)
        self.ui.Rod_wiget.cellChanged.connect(self.Provirka)
        self.ui.Node_wiget.cellChanged.connect(self.provirka)
        self.Rod_list = []
        self.Node_list = []
        self.ui.checkBox.clicked.connect(self.Lz)
        self.z = 0
        self.ui.checkBox_2.clicked.connect(self.Rz)
        self.Picture = QGraphicsScene()
        self.ui.graphicsView.setScene(self.Picture)
        self.ui.pushButton_2.clicked.connect(self.Otr)
        self.ui.action.triggered.connect(self.file_save)
        self.ui.action_2.triggered.connect(self.file_open)
        self.load_flag = False
        self.ui.pushButton_2.clicked.connect(self.processor)
        self.U = []





    def file_save(self):
        name = QFileDialog.getSaveFileName(self,"Save File",filter="*.txt")[0]
        if name != "":
            file = open(name, 'w')
            file.write(f"Параметры {len(self.Rod_list)} стержней"  )
            for i in self.Rod_list:
                file.write("\n")
                for j in i:
                    file.write(str(j)+" " )
            file.write(f"\nПараметры {len(self.Node_list)}  узлов ")
            for i in self.Node_list:
                file.write("\n")
                for j in i:
                    file.write(str(j) + " ")
            if self.z == 1:
                file.write("\nЛевая заделка")
            elif self.z == 2:
                file.write("\nПравая заделка")
            elif self.z == 3:
                file.write("\nОбе заделки")
            else:
                file.write("\nНет заделок")

            file.close()


    def file_open(self):

        fname = QFileDialog.getOpenFileName(self, 'Open file')[0]
        if fname!="":

            f = open(fname, 'r')

            with f:
                Rdata = f.readline()
                res = [int(i) for i in Rdata.split() if i.isdigit()]
                self.Rod_list.clear()
                self.load_flag = True
                for i in range(self.ui.Rod_wiget.rowCount()):
                    self.ui.Rod_wiget.removeRow(0)
                for i in range(self.ui.Node_wiget.rowCount()):
                    self.ui.Node_wiget.removeRow(0)
                for i in range(res[0]):
                    test = f.readline()
                    res = [float(i) for i in test.split() if float(i)]
                    while len(res)<5:
                        res.append(0.0)
                    self.Rod_list.append(res)
                    self.ui.Rod_wiget.insertRow(self.ui.Rod_wiget.rowCount())
                for i in range(len(self.Rod_list)):
                    for j in range(len(self.Rod_list[0])):
                        self.ui.Rod_wiget.setItem(i,j,QTableWidgetItem(f"{self.Rod_list[i][j]}"))        #хуета

                Ndata = f.readline()
                res = [int(i) for i in Ndata.split() if i.isdigit()]
                self.Node_list.clear()
                for i in range(res[0]):
                    test = f.readline()
                    res = [float(i) for i in test.split() if float(i)]
                    while len(res)<2:
                        res.append(0)
                    res[0]=int(res[0])
                    self.Node_list.append(res)


                    self.ui.Node_wiget.insertRow(self.ui.Node_wiget.rowCount())
                for i in range(len(self.Node_list)):
                    for j in range(len(self.Node_list[0])):
                        self.ui.Node_wiget.setItem(i,j,QTableWidgetItem(f"{self.Node_list[i][j]}"))
                self.ui.checkBox_2.setCheckState(0)
                self.ui.checkBox.setCheckState(0)
                Zdata = f.readline()
                self.z=0
                if Zdata == "Левая заделка":
                    self.ui.checkBox.setCheckState(2)
                    self.z+=1
                elif Zdata == "Правая заделка":
                    self.ui.checkBox_2.setCheckState(2)
                    self.z+=2
                elif Zdata == "Обе заделки":
                    self.ui.checkBox_2.setCheckState(2)
                    self.ui.checkBox.setCheckState(2)
                    self.z+=3
                self.load_flag=False










    def Lz(self):
        if self.ui.checkBox.checkState():
            self.z+=1
        else:
            self.z-=1

    def Rz(self):
        if self.ui.checkBox_2.checkState():
            self.z += 2
        else:
            self.z -= 2



    def dobR(self):
        self.ui.Rod_wiget.insertRow(self.ui.Rod_wiget.rowCount())
        self.Rod_list.append([0,0,0,0,0])

    def dobN(self):
        self.ui.Node_wiget.insertRow(self.ui.Node_wiget.rowCount())
        self.Node_list.append([0, 0])





    def Del(self):
        self.ui.Rod_wiget.removeRow(self.ui.Rod_wiget.rowCount()-1)
        try:self.Rod_list.pop()
        except: return

    def DelN(self):
        self.ui.Node_wiget.removeRow(self.ui.Node_wiget.rowCount()-1)
        try: self.Node_list.pop()
        except: return

    def Provirka(self):
        if self.load_flag == False:
            p = self.ui.Rod_wiget.currentItem().text()
            try:
                self.Rod_list[self.ui.Rod_wiget.currentRow()][self.ui.Rod_wiget.currentColumn()] = float(p)
            except:
                ms = QtWidgets.QMessageBox()
                ms.setIcon(QtWidgets.QMessageBox.Critical)
                ms.setText("     Ошибка    ")
                ms.setInformativeText('Недопустимое значение')
                ms.setWindowTitle("Error")
                ms.exec_()





    def provirka(self):
        if self.load_flag == False:

            p = self.ui.Node_wiget.currentItem().text()
            try:
                self.Node_list[self.ui.Node_wiget.currentRow()][self.ui.Node_wiget.currentColumn()] = float(p)
                if self.ui.Node_wiget.currentColumn() == 0:

                    self.Node_list[self.ui.Node_wiget.currentRow()][self.ui.Node_wiget.currentColumn()] = int(p)
                    if  int(p) <= 0 or int(p) > self.ui.Rod_wiget.rowCount()+1:
                        self.ui.Node_wiget.removeRow(self.ui.Node_wiget.currentRow())
                        print(self.Node_list)

                        raise Exception()

                else: pass
            except:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setText("     Ошибка    ")
                msg.setInformativeText('Недопустимое значение')
                msg.setWindowTitle("Error")
                msg.exec_()


    def Otr(self):
        self.Picture.clear()
        l = sum([i[0] for i in self.Rod_list])
        node=[0]
        try:
            h = max([i[2] for i in self.Rod_list]) #добавить проверку на 0 в списке
        except:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("     Ошибка    ")
            msg.setInformativeText('не задана площадь сечения')
            msg.setWindowTitle("Error")
            msg.exec_()
        if l != 0 and h != 0:
            k = self.ui.graphicsView.width()/l*0.9
            xl=0
            kl = self.ui.graphicsView.height() / h * 0.7
            avl = k*l*0.9 / self.ui.Rod_wiget.rowCount()
            for i in range(len(self.Rod_list)):  ##Нужен ли -1
                self.Picture.addRect(xl,0-kl*self.Rod_list[i][2]/2,k*self.Rod_list[i][0],kl*self.Rod_list[i][2])
                self.load(xl, k * self.Rod_list[i][0]+xl, self.Rod_list[i][4])

                xl+=k*self.Rod_list[i][0]
                node.append(xl)

            if self.z==1:
                self.Picture.addLine(0, -kl * self.Rod_list[0][2] / 2 * 1.1, 0, kl * self.Rod_list[0][2] / 2 * 1.1)
                self.Left_z(kl*self.Rod_list[0][2]*1.1)
            elif self.z==2:
                self.Picture.addLine(self.ui.graphicsView.width() * 0.9,
                                     -kl * self.Rod_list[self.ui.Rod_wiget.rowCount() - 1][2] / 2 * 1.1,
                                     self.ui.graphicsView.width() * 0.9,
                                     kl * self.Rod_list[self.ui.Rod_wiget.rowCount() - 1][2] / 2 * 1.1)
                self.Right_z(kl * self.Rod_list[self.ui.Rod_wiget.rowCount()-1][2] * 1.1,self.ui.graphicsView.width()*0.9)
            elif self.z ==3:
                self.Picture.addLine(self.ui.graphicsView.width() * 0.9,
                                     -kl * self.Rod_list[self.ui.Rod_wiget.rowCount() - 1][2] / 2 * 1.1,
                                     self.ui.graphicsView.width() * 0.9,
                                     kl * self.Rod_list[self.ui.Rod_wiget.rowCount() - 1][2] / 2 * 1.1)
                self.Picture.addLine(0, -kl * self.Rod_list[0][2] / 2 * 1.1, 0, kl * self.Rod_list[0][2] / 2 * 1.1)
                self.Left_z(kl * self.Rod_list[0][2] * 1.1)
                self.Right_z(kl * self.Rod_list[self.ui.Rod_wiget.rowCount()-1][2] * 1.1,self.ui.graphicsView.width() * 0.9)
            for i in range(len(self.Node_list)):
                if self.Node_list[i][0]<=self.ui.Rod_wiget.rowCount()+1:
                    self.loadqx(node[self.Node_list[i][0]-1],avl,self.Node_list[i][1])


#Единичные силы
    def loadqx(self, x,av, qx):
        if qx<0:
            pen = QPen(Qt.blue,2.0)
            xs =  av/10
            self.Picture.addLine(x, 0, x-xs, 0,pen )
            h=xs/5



            self.Picture.addLine(x-xs, 0, x-xs+xs/5, h, pen)
            self.Picture.addLine(x-xs, 0, x-xs+xs/5,-h, pen)
        elif qx>0:

            pen = QPen(Qt.red,2.0)

            xs = av / 10
            self.Picture.addLine(x, 0, x + xs, 0, pen)
            h = xs / 5

            self.Picture.addLine(x + xs, 0, x + xs -xs / 5, h, pen)
            self.Picture.addLine(x + xs, 0, x + xs -xs/ 5, -h, pen)



    def load(self,x,x1,F):

        if F<0:
            pen = QPen(Qt.blue)
            self.Picture.addLine(x, 0, x1, 0,pen)
            h=(x-x1)*0.1/5
            xs=(x-x1)/10

            for i in range(10):
                self.Picture.addLine(x-xs*i, 0, x-xs*i-xs/2, h, pen)
                self.Picture.addLine(x-xs*i, 0, x-xs*i-xs/2,-h, pen)
        elif F>0:
            h = (x - x1) * 0.1 / 5
            pen = QPen(Qt.red)
            self.Picture.addLine(x, 0, x1, 0,pen )
            xs = (x - x1) / 10


            for i in range(10):
                if i!=0:
                    self.Picture.addLine(x - xs * i - xs/3, 0, x-xs*i , h, pen )
                    self.Picture.addLine(x - xs * i - xs/3, 0, x-xs*i, -h, pen  )







    def Left_z(self,h):
        h1 = h / 7
        h = -h / 2
        for i in range(8):
            self.Picture.addLine(0, h, 0 - h1, h - (h1))
            h += h1

    def Right_z(self,h,x):
        h1 = h / 7
        h = -h / 2
        for i in range(8):
            self.Picture.addLine(x, h, x + h1, h + (h1))
            h += h1


    def processor(self):
        if self.ui.Rod_wiget.rowCount()>0 and all(self.Rod_list[i][0]!=0 for i in range(len(self.Rod_list))):           # Проверка на не нулевую длинну и на наличие стержня
            A = np.eye(self.ui.Rod_wiget.rowCount()+1)
            b = np.zeros(shape=(self.ui.Rod_wiget.rowCount()+1,1))
            force=np.zeros(shape=(self.ui.Rod_wiget.rowCount()+1,1))
            qxforce = np.zeros(shape=(self.ui.Rod_wiget.rowCount() + 1, 1))
            for i in range(len(self.Node_list)):
                force[self.Node_list[i][0]-1] = self.Node_list[i][1]

            b+=force
            for i in range(len(self.Rod_list)):
                qxforce[i]+=self.Rod_list[i][4]
            qxforce[-1]+=qxforce[-2]
            for i in  range(len(self.Rod_list)-1,0,-1):
                qxforce[i]+=self.Rod_list[i-1][4]
            b+=qxforce/2

            for i in range(self.ui.Rod_wiget.rowCount()):
                A[i][i] = self.Rod_list[i][1] * self.Rod_list[i][2] / self.Rod_list[i][0]
                A[i+1][i]=-A[i][i]
                A[i][i+1]=A[i+1][i]
            A[self.ui.Rod_wiget.rowCount()][self.ui.Rod_wiget.rowCount()]=A[self.ui.Rod_wiget.rowCount()-1][self.ui.Rod_wiget.rowCount()-1]
            for i in range(self.ui.Rod_wiget.rowCount()-1,-1,-1):
                if i!=0:
                    A[i][i]=A[i][i]+A[i-1][i-1]
            if self.z==1:
                A[0][0]=1
                A[1][0]=0
                A[0][1]=0
            elif self.z==2:
                A[self.ui.Rod_wiget.rowCount()][self.ui.Rod_wiget.rowCount()]=1
                A[self.ui.Rod_wiget.rowCount()-1][self.ui.Rod_wiget.rowCount()] = 0
                A[self.ui.Rod_wiget.rowCount()][self.ui.Rod_wiget.rowCount()-1] = 0
            elif self.z == 3:
                A[0][0] = 1
                A[1][0] = 0
                A[0][1] = 0
                A[self.ui.Rod_wiget.rowCount()][self.ui.Rod_wiget.rowCount()] = 1
                A[self.ui.Rod_wiget.rowCount() - 1][self.ui.Rod_wiget.rowCount()] = 0
                A[self.ui.Rod_wiget.rowCount()][self.ui.Rod_wiget.rowCount() - 1] = 0

            try: delta = np.linalg.solve(A,b)
            except: return
           # print(b)
          #  print(A)
          #  print(delta)
            #    A[i][i]=self.Rod_list[0][1]*self.Rod_list[0][2]/self.Rod_list[0][0]
                # A[i][i]=self.Rod_list[i][1]*self.Rod_list[i][2]/self.Rod_list[i][0]+A[i-1][i-1]
                    #A[i+1][i]=-(A[i][i]-A[i-1][i-1])
                    #A[i][i+1]=A[i+1][i]
            U = []
            U.append(*delta[0])
            for i in range(len(delta)-2):
                U.append(*delta[i+1])
                U.append(*delta[i+1])
            U.append(*delta[-1])
            self.savep(qxforce,U)
            #self.ux_ret(float(self.Rod_list[0][3]))
            step = 0.01             #шаг дискретизации на графике
            x=np.arange(0,sum([i[0] for i in self.Rod_list])+step,step)
            y=[]

            for i in x:
               y.append(self.sigm_ret(i))
            plt.plot(x,y)
            plt.show()

    def savep(self,qx,u):

        self.U=u


    def nx_ret(self,x):

        res = self.rod_conventer(x)
        return self.nx(res[0],res[1],res[2],res[3],res[4])





    def nx(self,U1,U2,x,n,qx):

        return self.Rod_list[n][1] * self.Rod_list[n][2]/self.Rod_list[n][0]*(U2-U1)+qx*self.Rod_list[n][0]/2*(1-2*x/self.Rod_list[n][0])

    def rod_conventer(self,x):              #Основная часть преобразований
        if x<=sum([i[0] for i in self.Rod_list]):

            i=0
            #nq=0
            if x == 0:
                i+=1
                x-=float(self.Rod_list[i][0])
            while x>0:
               x-=self.Rod_list[i][0]
               i+=1
            #if x!=0:
             #   nq=
            i-=1
            x+=float(self.Rod_list[i][0])

            res =[self.U[2*i],self.U[2*i+1],x,i,self.Rod_list[i][4]]    # U1 - начало U2- конец стержня, координаты относительно начала стержня, номер стержня, его продольная нагрузка
            return res

#Дебаг
    def ux_ret(self,x):
        if x<=sum([i[0] for i in self.Rod_list]):
            print(x)
            res=self.rod_conventer(x)
            print(res[0],res[1],res[2],res[3],res[4])
            return self.ux(res[0],res[1],res[2],res[3],res[4])

    def ux(self,U1,U2,x,n,qx): #U1 - начало U2- конец стержня
        return ((1-x/self.Rod_list[n][0])*U1+((x*U2)/self.Rod_list[n][0])+(((qx*self.Rod_list[n][0]**2*x)/(2*self.Rod_list[n][1] * self.Rod_list[n][2]*self.Rod_list[n][0]))*(1-x/self.Rod_list[n][0])))


    def sigm(self, U1, U2, x, n, qx):
        return (self.Rod_list[n][1] * self.Rod_list[n][2] / self.Rod_list[n][0] * (U2 - U1) + qx * self.Rod_list[n][
            0] / 2 * (1 - 2 * x / self.Rod_list[n][0]))/self.Rod_list[n][2]

    def sigm_ret(self,x):
        res = self.rod_conventer(x)
        return self.sigm(res[0], res[1], res[2], res[3], res[4])


app = QtWidgets.QApplication([])
application = mywindow()
application.show()
sys.exit(app.exec())
