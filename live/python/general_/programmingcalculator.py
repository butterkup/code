import tkinter
import tkinter.font
root=tkinter.Tk()
root.geometry('400x500')
root.title('calculator')
frame_above=tkinter.Frame(master=root,bg='black')
frame_below=tkinter.Frame(master=root,bg='black')

#functions
def ANS():
	ans_area['font']=text_area_font
	expression=text_area['text']
	if expression=='':
		return 0
	try:
		new_ans=eval(expression)
	except ZeroDivisionError:
		text_area['fg']='red'
		ans_area['fg']='red'
		ans_area['text']='math error'
	except:
		text_area['fg']='red'
		ans_area['fg']='red'
		ans_area['text']='syntax error'
	else:
		ans_area['fg']='black'
		ans_area['text']=str(new_ans)

def addvalue(value):
	if text_area['fg']=='red':
		text_area['text']=''
	if value=='remove_pre':
		text_area['text']=text_area['text'][:-1]
	elif value=='clear':
		text_area['text']=''
		ans_area['text']=''
	else:
		text_area['fg']='black'
		new_value=text_area['text']+value
		text_area['text']=new_value

def colorMybuttons():
	qui['bg']='#500000'
	qui['activebackground']='#990000'
	for common in [one,two,thr,plu,fou,fiv,six,sub,sev,eig,nin,mul,ope,zer,clo,div,qui,cle,det,ans]:
		common['fg']='white'
		common['activeforeground']='white'
		common['anchor']='nw'

	for special in [plu,ope,clo,sub,mul,div]:
		special['bg']='#005000'
		special['activebackground']='#009900'
		
	for special in [cle,ans,det]:
		special['bg']='#000000'
		special['activebackground']='#353535'

	for num in [one,two,thr,fou,fiv,six,sev,eig,nin,zer]:
		num['bg']='#000080'
		num['activebackground']='#0000ff'

ONE=lambda : addvalue('1')
TWO=lambda : addvalue('2')
THR=lambda : addvalue('3')
FOU=lambda : addvalue('4')
FIV=lambda : addvalue('5')
SIX=lambda : addvalue('6')
SEV=lambda : addvalue('7')
EIG=lambda : addvalue('8')
NIN=lambda : addvalue('9')
ZER=lambda : addvalue('0')

PLU=lambda : addvalue('+')
SUB=lambda : addvalue('-')
MUL=lambda : addvalue('*')
DIV=lambda : addvalue('/')
OPE=lambda : addvalue('(')
CLO=lambda : addvalue(')')

CLE=lambda : addvalue('clear')
DEL=lambda : addvalue('remove_pre')
QUI=lambda: root.destroy()


#above frame widgets
text_area_font=tkinter.font.Font(family='freemono',weight='bold',size=25)

text_area=tkinter.Label(master=frame_above,font=text_area_font,anchor='nw')
text_area.place(relx=0,rely=0,relheight=0.1,relwidth=1.0)

welcome_and_goodbye_font=tkinter.font.Font(family='cursive',size=25,weight='bold')

ans_area=tkinter.Label(master=frame_above,font=welcome_and_goodbye_font,anchor='ne')
ans_area.place(relx=0,rely=0.1,relheight=0.1,relwidth=1.0)

frame_above.place(relx=0,rely=0,relheight=1.0,relwidth=1.0)
frame_below.place(relx=0,rely=0.2,relheight=1.0,relwidth=1.0)

#below frame widgets
#number buttons
one=tkinter.Button(master=frame_below,text='1',command=ONE)
two=tkinter.Button(master=frame_below,text='2',command=TWO)
thr=tkinter.Button(master=frame_below,text='3',command=THR)
fou=tkinter.Button(master=frame_below,text='4',command=FOU)
fiv=tkinter.Button(master=frame_below,text='5',command=FIV)
six=tkinter.Button(master=frame_below,text='6',command=SIX)
sev=tkinter.Button(master=frame_below,text='7',command=SEV)
eig=tkinter.Button(master=frame_below,text='8',command=EIG)
nin=tkinter.Button(master=frame_below,text='9',command=NIN)
zer=tkinter.Button(master=frame_below,text='0',command=ZER)

#signs buttons
plu=tkinter.Button(master=frame_below,text='+',command=PLU)
sub=tkinter.Button(master=frame_below,text='-',command=SUB)
mul=tkinter.Button(master=frame_below,text='*',command=MUL)
div=tkinter.Button(master=frame_below,text='/',command=DIV)
ope=tkinter.Button(master=frame_below,text='(',command=OPE)
clo=tkinter.Button(master=frame_below,text=')',command=CLO)


#other special buttons
ans=tkinter.Button(master=frame_below,text='ANS',command=ANS)
det=tkinter.Button(master=frame_below,text='DEL',command=DEL)
cle=tkinter.Button(master=frame_below,text='CLEAR',command=CLE)
qui=tkinter.Button(master=frame_below,text='EXIT',command=QUI)

#place the buttons
buttons=[one,two,thr,plu,fou,fiv,six,sub,sev,eig,nin,mul,ope,zer,clo,div,qui,cle,det,ans]
button=0
for Y in [0,0.16,0.32,0.48,0.64]:
	for X in [0,0.25,0.5,0.75]:
		buttons[button].place(relx=X,rely=Y,relheight=0.16,relwidth=0.25)
		button+=1
colorMybuttons()

root.mainloop()