from direct.showbase.ShowBase import ShowBase







class mainApp(ShowBase):

    def __init__(self,debug):
        super(mainApp,self).__init__()
        
        if debug == True:
            from configs.configs import debug_mode 
            debug_mode.test_run() 
            



    
        




def main():
    
    app = mainApp(debug=True)
    app.run()




if __name__ == '__main__':
    main()
