style = """
QWidget{
    background:rgb(35,35,35)
}
QPushButton{
    background:rgb(55,55,55);
    border-radius:5px;
    color:white;
    padding:5px
}QPushButton:hover{
    background:rgb(40,40,40);
    border:1px solid rgb(10,10,10)
}
QComboBox{
    background:rgb(100,100,100);
    border-radius:5px;
    padding:3px;
    color:white;
}
QComboBox QAbstractItemView{
    background:rgb(100,100,100); 
    padding:3px;
    outline:none;
}
QListWidget{
    border:1px solid rgb(90,90,90);
    border-radius:5px;
    color:white;
    outline:none
}
QListView::item,QListWidget::item{
    outline:none;
    border-radius:5px;
    padding-left:3px;
    border:1px solid transparent;
}QListView::item:hover,QListWidget::item:hover{
    background:rgb(50,50,50);
    border:1px solid rgb(10,10,10)
}QListView::item:focus,QListWidget::item:focus{
    color:white;
}
QLabel{
    color:white
}QMessageBox{
    background:rgb(35,35,35)
}
QScrollBar::handle{
    background:rgb(45,45,45);
    border-radius:7px;
}
QScrollBar::handle:hover{
    background:rgb(40,40,40);
}
QScrollBar::handle:pressed{
    background:rgb(30,30,30)
}
QScrollBar::add-line,QScrollBar::sub-line,QScrollBar::add-page,QScrollBar::sub-page{
    border:none;
    background:rgb(35,35,35);
    border-radius:7px;
}
"""