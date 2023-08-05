from select import select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

class wrapper:

    def __init__(self, browser):
        self.browser = browser

    def findElementsBy(self, xpath):
        # self.browser.presence_of_all_elements_located(xpath)
        # self.browser.visibility_of_element_located(xpath)
        return self.browser.find_elements(By.XPATH, xpath)

    def findElementBy(self, xpath):
        self.browser.presence_of_element_located(xpath)
        self.browser.visibility_of_element_located(xpath)
        self.browser.find_element(By.XPATH, xpath)

    def click(self, xpath, index=None):
        self.browser.visibility_of_element_located(xpath)
        self.browser.element_to_be_clickable(By.XPATH, xpath)
        self.browser.find_element(By.XPATH, xpath).click()

    def isClickable(self, xpath, index=None):
        # self.browser.visibility_of_element_located(xpath)
        return WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
    # fill input or text area field

    def fillField(self, xpath, text):
        self.browser.presence_of_element_located(xpath)
        self.browser.visibility_of_element_located(xpath)
        self.browser.find_element(By.XPATH, xpath).send_keys(text)
    # drop downs

    def selectDropDownByValue(self, xpath, valueToSelect):
        self.browser.presence_of_element_located(xpath)
        self.browser.visibility_of_element_located(xpath)
        select = Select(self.browser.find_element(By.XPATH, xpath))
        select.select_by_value(valueToSelect)

    def selectDropDownByIndex(self, xpath, indexToSelect):
        self.browser.presence_of_element_located(xpath)
        self.browser.visibility_of_element_located(xpath)
        select = Select(self.browser.find_element(By.XPATH, xpath))
        select.select_by_index(indexToSelect)

    def selectDropDownByVisibleText(self, xpath, textToSelect):
        self.browser.presence_of_element_located(xpath)
        self.browser.visibility_of_element_located(xpath)
        select = Select(self.browser.find_element(By.XPATH, xpath))
        select.select_by_visible_text(textToSelect)

    def deselectAllOptionsInDropDown(self, xpath):
        self.browser.presence_of_element_located(xpath)
        self.browser.visibility_of_element_located(xpath)
        select = Select(self.browser.find_element(By.XPATH, xpath))
        select.deselect_all()

    def getDefaultSelectedDropDownOptions(self, xpath):
        self.browser.presence_of_element_located(xpath)
        self.browser.visibility_of_element_located(xpath)
        select = Select(self.browser.find_element(By.XPATH, xpath))
        all_selected_options = select.all_selected_options
        return all_selected_options

    def getAllOptionInDropDown(self, xpath):
        self.browser.presence_of_element_located(xpath)
        self.browser.visibility_of_element_located(xpath)
        select = Select(self.browser.find_element(By.XPATH, xpath))
        options = select.options
        return options
    # drag and drop

    def dragAndDrop(self, sourcexpath, destinationxpath):
        sourceElement = self.browser.find_element(By.XPATH, sourcexpath)
        destination = self.browser.find_element(By.XPATH, destinationxpath)
        action_chains = ActionChains(self.browser)
        action_chains.drag_and_drop(sourceElement, destination).perform()

    def dragAndDropByOffset(self, sourcexpath, xoffset, yoffset):
        sourceElement = self.browser.find_element(By.XPATH, sourcexpath)

        action_chains = ActionChains(self.browser)
        action_chains.drag_and_drop_by_offset(
            sourceElement, xoffset, yoffset).perform()
    # switch to window
    # ex: <a href="somewhere.html" target="windowName">Click here to open a new window</a>

    def switchToWindowUsingName(self, windowName):
        self.browser.switch_to_window(windowName)

    def switchtoWindowUsingHandle(self, windowNumber):
        current_window = self.browser.current_window_handle
        ListOfHandles = self.browser.window_handles
        if(current_window != ListOfHandles[windowNumber]):
            self.browser.switch_to.window(ListOfHandles[windowNumber])
    # frame switch, It’s possible to access subframes by separating the path with a dot,
    # and you can specify the frame by its index too. That is: driver.switch_to_frame("frameName.0.child")
    # would go to the frame named “child” of the first subframe of the frame called “frameName”. All frames are evaluated as if from *top*.

    def swithToFrame(self, frameName):
        self.browser.driver.switch_to_frame(frameName)
    # Once we are done with working on frames, we will have to come back to the parent
    # frame which can be done using:

    def swithToParentFrame(self):
        self.browser.switch_to_default_content()
    # navigating

    def navigateto(self, urlstring):
        self.browser.get(urlstring)
    # action class

    def actionClick(self, xpath):
        actions = ActionChains(self.browser)
        element = self.browser.find_element(By.XPATH, xpath)
        actions.click(element)

    def actionClickandHold(self, xpath=None):
        actions = ActionChains(self.browser)
        if(xpath != None):
            element = self.browser.find_element(By.XPATH, xpath)
        else:
            element = None
        if(element != None):
            actions.click_and_hold(element)
        else:
            actions.click_and_hold()

    def moveToElement(self, xpath):
        actions = ActionChains(self.browser)
        element = self.browser.find_element(By.XPATH, xpath)
        actions.move_to_element(element).perform()

    def moveToElementWithOffset(self, xpath, xoffset, yoffset):
        actions = ActionChains(self.browser)
        element = self.browser.find_element(By.XPATH, xpath)
        actions.move_to_element_with_offset(element, xoffset, yoffset)

    def moveByOffsett(self, xoffset, yoffset):
        actions = ActionChains(self.browser)
        actions.move_by_offset(xoffset, yoffset)

    def actionRelease(self, xpath=None):
        actions = ActionChains(self.browser)
        if(xpath != None):
            element = self.browser.find_element(By.XPATH, xpath)
        else:
            element = None
        if(element != None):
            actions.release(element)
        else:
            actions.release()

    def keyDown(self, ModifierKey, key, xpath=None):
        actions = ActionChains(self.browser)
        if(xpath != None):
            element = self.browser.find_element(By.XPATH, xpath)
        else:
            element = None
        if(element != None):
            actions.key_down(ModifierKey, element).send_keys(key)
        else:
            actions.key_down(ModifierKey).send_keys(key)

    def keyUp(self, ModifierKey, key, xpath=None):
        actions = ActionChains(self.browser)
        if(xpath != None):
            element = self.browser.find_element(By.XPATH, xpath)
        else:
            element = None
        if(element != None):
            actions.key_up(ModifierKey, element).perform()
        else:
            actions.key_up(ModifierKey).perform()

    def double_click(self, xpath: None):
        actions = ActionChains(self.browser)
        if(xpath != None):
            element = self.browser.find_element(By.XPATH, xpath)
        else:
            element = None
        if(element != None):
            actions.double_click(element)
        else:
            actions.double_click()

    def righttClick(self, xpath=None):
        actions = ActionChains(self.browser)
        if(xpath != None):
            element = self.browser.find_element(By.XPATH, xpath)
        else:
            element = None
        if(element != None):
            actions.context_click(element)
        else:
            actions.context_click()
    def resetActions(self):
        actions = ActionChains(self.browser)
        actions.reset_actions()
    def sendKeys(self,*keys_to_send):
        actions = ActionChains(self.browser)
        actions.send_keys(keys_to_send)
    def sendKeysToElement(self,xpath, *keys_to_send):
        actions = ActionChains(self.browser)
        element = wrapper.webdriverWait(self,xpath)
        actions.send_keys_to_element(element,keys_to_send)

    #alerts
    # Use this class to interact with alert prompts. 
    # It contains methods for dismissing, accepting, inputting, and getting text from alert prompts.   
    def acceptAlert(self):
        Alert(self.browser).accept()
    def dismissAlert(self):
        Alert(self.browser).dismiss() 
    def getAlertText(self):
        alertText=Alert(self.browser).text
        return alertText
    def sendKeystoAlert(self,keysToSend):
        name_prompt = Alert(self.browser)
        name_prompt.send_keys(keysToSend)
    # Special Keys
    #The Keys implementation.
    ''' yet to complete'''
    #Touch Actions
    ''' yet to complete'''
    #select tag
    #dropdown
    def deselectByIndex(self,xpath,index):       
        select = Select(self.browser.find_element(By.XPATH, xpath))
        select.deselect_by_index(index)
    def deselectByValue(self,xpath,value):       
        select = Select(self.browser.find_element(By.XPATH, xpath))
        select.deselect_by_value(value)        
    def deselectByVisibleText(self,xpath,text):       
        select = Select(self.browser.find_element(By.XPATH, xpath))
        select.deselect_by_visible_text(text)
    def getFirstSelecteOption(self,xpath):
        select = Select(wrapper.webdriverWait(self,xpath))
        return select.first_selected_option
    #Wait Support
    #
    def webdriverWait(self,xpath):
        return WebDriverWait(self.browser, 10).until(lambda x: x.find_element(By.xpath, xpath)) 





