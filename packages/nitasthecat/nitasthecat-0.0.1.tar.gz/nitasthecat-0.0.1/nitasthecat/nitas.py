import webbrowser

class Nitas:
    """
    This class is for my dearest friend "Nitas"
    Who he is
    his age
    his website

    Example:
    ----------------
    cat = Nitas()
    cat.show_name()
    cat.about()
    cat.show_mypic()
    cat.show_youtube
    cat.show_IG()
    ----------------
    """
    def __init__(self):
        self.name = "Nitas"
        self.species = "F.catus"
        self.breed = "Persian"
        self.age = 7
        self.IG = "https://www.instagram.com/nitasthecat/"

    def show_name(self):
        print(f"Hi my name is {self.name}")

    def about(self):
        text = f"""
        -------------------------------------------------------------------------
        My name is nitas. Yes im just a cat! a {self.breed} cat :p
        I'm {self.age} years old.
        -------------------------------------------------------------------------
        I belong to the {self.species} species.Yes I'm just a little fluffy friend.
        If you want to know more about me type help(Nitas) and find my
        other detail about me in another method.

        """
        print(text)

    def show_youtube(self, open= False):
        url = "https://www.youtube.com/channel/UCkRESzH67VQHT0vh5p-sPHQ"
        print(url)
        if open == True:
            webbrowser.open(url)
    
    def show_IG(self, open= False):
        print(self.IG)
        if open == True:
            webbrowser.open(self.page)

    def show_mypic(self):
        text = """
                               '.........''......'''''....                                ...',;:okOOo.    .;;',,,,,;;'.;:c:;;;;
                      .,,........''.......'.'..                              ....''',:ok0Okkkd;....;;'.'''.''...;c:;;,,,
                       ,odoc;'....'.........'..                          ..'',,,,,;:ok0Oxdoodo:,,,,;,''''''.............
                  .    'd0000ko;'''.........'..                       ..',,,,,,,;:lk0Oxxdddooo:;;;,,;;;;,,,'....  ..  . 
                 .....';okkkOO0Oxl;''',,..'.'..             ..........',,,,,,,;:ok0Okxddooooooc;;;;;;;;;;;;,,,,'..'',:cl
        ........'',,;cloxkxxkkkO00kl:cc:'.'.'..      ...........''''',',;::;;:ok00Okxddooddooolcllcc:;;;,,,,,,;;;;,;:lod
.............',:ccccc:clxkkkkkkxxkOOkdl:'.'''.. .........'.''''',,,,;:ccldkkkOKK0kxxxddddddddddoolc:;;;;;,,,,,,;;;;;;;;;
,;;;:::;,;;;::ccccllllccldxxkkxxxxxxO00Odlllc;,,,,,;;,,',:;;::::codxkOKKKXXNNX0Okkxxdddddddddllc:;;,,,,,,,,,,,,,,;,;;;;;
:ccccccccccccccc::::::coddxxxxxxxdxxxkOKXNXXXK000OxxxxxddkOO0OOOOKXNNNNNNNNNX0Okxxdddddddollc::;;;;;;;;,,,,,,,,,,,,,,;;;
:ccccc:::;,,''......',;codddddxxxxxxxxkO0XNNWNNWNNNNNNNNNNNXXXXXNNNNNWWWNNNX0Okxxdddddollcllcccccc::;;;;;;;;;,,,,,,,,,,;
:,'..''........',,;;:lclllodddddddxxxxxkO0XNNNNNNNN::NNNXXK0Ok::::NNNNNNNNXK0OOkxxxdoollllooolcc:::;;;;;;;;;;;;;;;,,,;;;
:'...',::::lodxkkkkxkkdlllodddddoodddddxkOKXXXXXX::::OKXNNXKKOk::::NNNNNNNXK00OOOkxddddooodoc:;;;;;;;::;;;;;;;;;;;;;;;;;
;';ldxxkOOOkkkkxoc:;;,,;cccoddddddodxxxxkOKKKK0O:::::KNNNNNNXKK:::NNNNNNXXK000Okkxxxxxdloddol:;,,,;;;;::::::::;;;;;;;;;
'.,lxlccccc:;;,,'..',,;:cldxkdoodxxdxkkkkO000O:::::OKXNNNNNNNNNNXNNNNNNNNXXKK0Okkkxxxxdlcoxkxo:,,'',,,,;;;::::::::::;;;;
l:;;;;,''''',''',,,;;::cldk0KOdoddxkxxkOO0000Ok::::XNNNNNNNNNNNNXNNNXXXXXXXXK00Okkkxxdlccoxdolc:;,''''',,,;;;:::::::::::
o::c;:llccc:;;,,,,;;::cldk0KXKxoodxxkkkO000000KKKXXNNNNNNNNNNNNNXNNNXXKKKXXXKKK00OOkxdolodxxddol;'.....'''',,,;;;:::::::
cc:;;;;;;,,,,,''',;:lodxk0KXXX0xdodxkO00KKKKXXXXXXXXXNNNNXXXXXXXXXNXXXXXXXXXXKKKKK00Okkxxxxxxdoc;'..........'',,,,;;;;::
,,''''''''''''',;:ccccoxO0KKKKKOkxxkOKKXXXXXXXXXXXXXXXXXXXKKXXXXXKKKKKKXKK0000KKKKKKKKK00OOkkxdoc,'............'''',,,;;
'''''''''''',,;;:::cccldk0KKK000000KKKXXXXXKK0000KKKKK000KKKKKKKK0OOkkxxxdolloxkO00KKKKKKK00OOkxl;'.................''',
''''''',,,,,,;;;;;;::clxO0KKKKKKXXXXXXXXKKOxolclodkkxkkkkOO00000Okdoolc;'.....';ldxO0KKXXXK0OOkkdl;.....................
,,,,,,,,,,,;;;;;;;;:clok0KKKKKKXXXXNXXK0ko:'......;cooodxxkkkkkxdolcc:..   .....':ldOO00KKK00Okkxdc,....................
;;;;;;;;;;;;;;;;;;;;:clk0KKKKXXXXXXXXKOdc;.....  ...;clodxkkkkxolc::;..       ..':ok00000000OOkxxdl;'...................
;;;;;;;;;;;;;;;;;;;::lx0KKKKXXXXXXXXXXKOo;..     ...'codkOOOOkxolc::,...... ....;okO00000Okxxxxdddoc,...................
;;::::::;;;;;;;;;:clldOKKKKKKKKKKKKXKXXXOl,.........,lxO0KKK00OOxdoo:'.......';ok0000OOOkxdddoddddol;'..................
::;;;;;;;;;;;;;;:oxkO0KXKKKKK0000KKKKXXXX0xl:;,,;:codxO0KXXXXXXXK0OkdlllooxkO0XNNXK0Okkxxxddddodddol;'..................
;;;;;;;;;;::::clloOXXXXXKKKK00OO0000KKXXXNNXXKKKKKK00KKKXXXXXXXXXXK0000KXXNNNNXXKK0Okxxddxxxxdddddoc,...................
;;;;:;;;;;;:::ok00XNNNXKKKKK00OO00000KKXXXXXXXXXXXXXXXKKKKXXXXXXK000KXXXXKKKK00OOkkxxxdddddddoooool:'...................
:;;;;;;;;;:coxOKNNWNNXXKKKKK00OO00OOO000K00000000KXXXXKOO0000000OxdxO0K00Oxxxxddddddoooooollllloll:,....................
;;;;;;;;;:::o0XNNNNNXXKKKKK00OOO0OOOOOOOkkxkkOOkO0KXXKOdlllcccc:;,,:xOOkkxddooolcccccccllllllllllc:,....................
;;;;;;;::::cd0NNWWNNXKKKKK00OOOOOOOOkkxddddxxkxkO0KKKX0kc'.',,''..,lxkkkOkkkxolcccccccccllllllllc:,.....................
;;;;;;::coxOKXNWWWNNXKKKK00OOOOOkkkkxxddddddxkO0000000Okxl;''''',;clooooodxxxdolccclllllllllllllc:'.....................
::::::::cx0NNNNWWWNXXXKK00OOOkkkkxxdddddoooxkOOOOkkkkkxdolc;,,,;::cclllllloooooolllllllllcclllolc:'.....................
::::::::lxKXNNNNNNXXXXKK00OOOkkkxxddooooddxkkOkkxxxddolcc:;,''',;:::cccccclllllllllllollllllllllc;'.....................
:::;;;::oOXXNNXXXXXXXXKK00000OOkxxdddddooddxxxddddoolcc::;;,,,,,,,;;;::ccccclllcccccccllllllllolc,......................
:::;;::lx0XXNXXXXXXXXXXKK000000OOkxxddooooooooooolllccc::::::::::;;;;;:::ccclccclccccccccccllool:,.........  ...........
:::::ccoOKXXXXXXXXXXXXKK00000000OOkxxddoooollloolllllccccccccccc::::::::ccccllcccccccccccccclll:,.........     .........
::ccclox0XNNNNXXXXXXXKK0000OO000OOOkxxdooolllollccccccccccccccccccc::::::cccccllcccccccc:ccccc:;'...........         ...
::clldk0XXXXNXXXXKKKK0000OOkkkOOOOkkxxddoollolllccccccccccccccccc:::::::::::ccclcccccccccccc::;,..............          
:cclxOKXNNNNNNNNXXXKK000OOOkkkkkkxxxxxxddooollllllcccccccccc::::::::::::::::cccccc::cccccccc;,..... ......  ....        
cccokKNNNNNNNNNNNXXXXKK00OOOkkxxxddxxxxxdodollllllcccccccccc:::::::::::::::::cccccc::::cccc:;'..       ....    ...      
codkKXNNNWWNNNNXXXXXXXKKK00Okxxxdddddddddoooollllllcccccccccccc::c::::::::::::::ccc::::cccc:,...         ...    ..      
okKXNNNNNNNNNNXXKKKKKKKKK0Okkxxddddddoooooooollllllccccccccccccccccccccc::::::::::::::::::;;,..           ...     ..    
OKNNNNNNNNNNNXXKKKKKKKK00OOkkkxxddoddoollooolllcccccccccccccc::cccccc::ccc::::::::::::::;'....              ..    ..    
KNNNNNNNNNNNNXXKK0000000OOOkkkxxdddddoolloolllcccllllcccccccccc::ccccc:::::::::::::::::;,'...                           
KXNNNNNNNXXXXXKKKK000KK0OOkxxxxxddddooollollllccllllcccccccccccc::cccccc:::cc::::::;;:;,...                   .         
KXXNNNXXXXXXXKKKKKK0KK0Okxxdxxxxddddoooollllclllllllccccllcccccc:::ccccccc:::::::::;;;,...                              
KXXXXXXXXXKKK000KKK00Okxxdxxkkkxxdddoooolllllllllllcccclllccccccc::cccccccc:::::::;;;,'...                              
XXXXXXXKKKKK000000000kxdxxkOOOkxddddooolllllllllllccccllllcccccccc:ccc:::cc:::::::;,,....                               
XXXXKKKKKKKK0OOOO0000OxxxkOOOkkxddoooololllllllllccc:ccllccccccccccccc:::::::::::;,'...                                 
KKKKKKK00KK00OkkkOO00Okxxxxkkkxddoooooollllllllllclcccccccccccccc:::ccc::::::::::;'...                                  
000KK0000000OkkxxkOOOOkxddddddooddooooollllllllccccc:cccccccccccc::::::::::;;;;;;;,..                                   
00KK0KKK000OkxxdxkOOkkkddooooloddodddolllllllclcclcc:cccccccccccc::::::::;;;;,,,'....                                   
O000000K00OOkddddxkkkxxddolllldxoodxoolllllccclllccccccc::cccc:::::;;;;;;;,,''.....                                     
OOO0000000Okdollodkkkkxdoollllollloolllclcccccccccc:::c:::::::::::;;;;,,,,''....                                        
xkkkOkkkkkxolcccldkOkkxdolllcccccccccccccccccccccc::::::::::::::;;;;;,,'''....                                          
oooodoooolcc:::ccldxkkxdollcccccccccc::::cccccccc:::::::::::::;;;,,,,'''.....                                           
lollllccccc::;;:;:codxxdolccccc::::::::::::c::::::::;;::;:;;;;;;,,'''''.....                                            
clllllcccc:;;,;;;;;:lddoolcc:::::::::::::;;:::::::::;;;;;;;,,,,,,'''''.....                                             
;:ccc::;::;;,,,,,;,;:lllllccc::::::;;;;;;;,,;,;;;;;;,,,,,,,,,,,''''''.....                                              
;;;;;;,,;;,,,,,,,,'';cllllcccc:::;;;;;;;;;,,,',;;,,,,,,,,,,,,,,'''''......                                              
        """
        print(text)
        

if __name__ == '__main__':
    cat = Nitas()
    cat.show_name()
    cat.about()
    cat.show_mypic()
    cat.show_youtube
    cat.show_IG()