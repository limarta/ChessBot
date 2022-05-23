from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
from engine import UCIBoard

'''
Finds the color of the bot
'''
def getColor(driver):
    color_js = """
    color = document.querySelectorAll('captured-pieces')[1].color;
    return color;
    """
    return driver.execute_script(color_js)-1

'''
Parses the html styling of moves and returns the moves in algebraic notation
'''
def parsePly(driver, ply):
    js = """
    console.log('Searching for ply """+ str(ply) +"""');
    move = document.querySelectorAll("div[data-ply='""" + str(ply) + """']")[0];
    if(move == null) {
        console.log('Found nothing');
        return 0;
    } 
    if (move.childNodes.length == 1) {
        return move.childNodes[0].data;
    } else {
        let piece = move.childNodes[0].dataset['figurine'];
        return piece + move.childNodes[1].data;
    }
    """
    # print(js)
    move = driver.execute_script(js)
    if move == 0:
        return None
    else:
        return move

    
def start_bot():
    board = UCIBoard()
    driver = webdriver.Chrome("./chromedriver")
    driver.get("https://www.chess.com/play/online")

    elements = driver.find_elements(by=By.CLASS_NAME, value="ui_v5-button-component")
    play = None
    for e in elements:
        if "Play" in e.get_attribute("innerHTML"):
            play = e 
            break
    play.click()

    time.sleep(1)
    driver.find_element(by=By.ID, value="guest-button").click()
    time.sleep(2)

    elements = driver.find_elements(by=By.CLASS_NAME, value="ui_v5-button-component")
    for e in elements:
        if "Ok" in e.get_attribute("innerHTML"):
            play = e
            break
    play.click()
    time.sleep(3)
    # In game now
    color = getColor(driver)
    print("My color: ", color)

    # Find captured-pieces tag. has color=1 or 2
    time.sleep(3)
    moves = []
    
    ply = 1
    while ply<300:
        if 1-(ply % 2) == color:
            if ply == 1:
                move = board.readAndReply()
            else:
                move = board.readAndReply(moves[-1])
            # TODO: Make move on board
        while True:
            move = parsePly(driver,ply)
            if move is not None:
                moves.append(move)
                break
            time.sleep(1)
        print(f"Moves on ply {ply}: {moves}")
        ply+=1

    time.sleep(100)
    driver.quit()


def movePiece():
    d = webdriver.Chrome('./chromedriver')
    d.get('https://www.chess.com/play/computer')
    time.sleep(10)
    board = d.execute_script('''
    function coords(elem){
        var n = elem.getBoundingClientRect()
        return {top:n.top, left:n.left, width:n.width, height:n.height}
    }
    var pieces = []
    for (var i = 1; i < 9; i++){
        if (i > 6 || i < 3){
            pieces.push(Array.from((new Array(8)).keys()).map(function(x){
            var square = document.querySelector(`.piece.square-${x+1}${i}`)
            return {...coords(square), piece:square.getAttribute('class').split(' ')[1]}
            }));
        }
        else{
            pieces.push(Array.from((new Array(8)).keys()).map(function(x){
            var arr = pieces[pieces.length-1]
            return {left:arr[x].left, top:arr[x].top - arr[x].height, 
                width:arr[x].width, height:arr[x].height, piece:null}
            }));
        }
    }
    return pieces
    ''')[::-1]

    from selenium.webdriver.common.action_chains import ActionChains
    def click_square(square):
        elem = d.execute_script('''return document.querySelector('body')''')
        print("Element: ", elem)
        ac = ActionChains(d)
        ac.move_to_element(elem).move_by_offset(300, 400).click().perform()

    piece = board[6][3]
    print(piece)
    click_square(piece)
    print("Done")
    time.sleep(100)
    d.quit()
if __name__=="__main__":
    movePiece()
    # start_bot()

