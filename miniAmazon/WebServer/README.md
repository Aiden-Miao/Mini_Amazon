# erss-final-prj-IG4
project: Mini Amazon, ERSS final project
Interoperability Group: group 4
author(s): 
- (Mini Amazon): Yating Li(yl657), Boayn Hou(bh214)
- (Mini Amazon): Aiden Miao(km480), Yuecong Lou(yl646)
- (Mini UPS): Eunbi Zhang(yz553), Mutian Wang(mw434)
- (Mini UPS): Zeyu Li(zl254), Kuan Wang(kw300)

### Amazon <-> UPS communication protocol
[google doc](https://docs.google.com/document/d/1gah2Sp8nS9R42Teq39cvFh6G-PHr9YUav5v72NxJN_A/edit?usp=sharing)


### Qs for TA:
~~- Q1: in `.proto:Aconnect`, why is the field `worldid` marked as optional? Does that mean Amazon can also create a new world?~~
~~- Q2: What are the formats that we should use to communicate with world server? JSON?~~  
~~- Q3: For `ACommands` and `AResponses`: do we have to wrap everything we want to communicate with the world server within these two classes?   
    e.g., if I have a `APurchaseMore` command, can I send it directly, or do I have to first put it in an `ACommands`?~~     
~~- Q4: what if Amazon user does not specify a UPS user id for an order? Does that mean this order is un-trackable on the UPS website, only trackable on Amazon?~~