# BioinformaticsCustomAmazonSkill

## Initial Plan

### The goal of this project is help researchers in the Biology Department have a constructive discussion about specific proteins and their structures, while simultaneously having a computer or AI run database searches, predict protein structures using machine learning models, and visualize all the information for everyone to see. We hope to achieve this goal by creating a custom Amazon Alexa skill. This project will have three phases in order to complete this goal. The first phase will be to create our custom code that is able to communicate with the protein database, run queries, and predict protein structures. This codebase will be hosted on AWS. The second part of this phase is preparing the initial setup of our custom skill with Alexa. We will have to design a voice user interface, that allows the user to request the skill using a set of pre determined phrases. This will be accomplished through tweaking the parameters of Amazon’s NLP models. The second phase will be to integrate our custom codebase with our Amazon skill. After the integration is successful, testing of the entire project will be executed in order to make sure the requests Alexa reads can be deciphered with our codebase. This will require further tweaking of the NLP model and changing our custom codebase to understand the request Alexa sends over the sever. The last phase is to implement the visualization feature for this skill. When requested, Alexa should display the results on the Alexa app or on the projector using Amazon’s smart home features. At this point, we should have a working prototype of our custom skill that can be used in house for researchers and professors to use. Future modifications such as user experience and efficiency can be done after the basic features are established. 

### USAGE : Must call the method get_proteins() and give the require parameters. only num and query are required for the query, everything else is optional. Also, everything must be sent as a list of strings except for num and query. I've written two short examples at the bottom of the script that is commented.




How to login:
* https://developer.amazon.com/
* Login using your Alexa developer account information. 

Navigation:
* Under the navigation bar, hover over "Alexa" and select "Alexa Skills Kit"
* This should transport you to the "Alexa developer console"
* Click on "UniProt Protein Search" to navigate to the developer portal for that skill

Editing:
* Invocation: How to start the search
  * "Start protein database" where protein database is the invocation you set   
* Intents: What the user says to cause an action
  * "look up brain" the lambda functions parses that the "webSearch" intent was used, with the search parameter "brain"
* Click "Save Model" then "Build Model"
 
Testing:
* Next Click "Test" near the top of the webpage
* You can test using the microphone (hold down the button, and verbal give your invocation and intents) or by typing them into the text box provided.
* Here are some examples of tests you can do and what they will return:

 * Type or say: "start protein database"
  * Return: "Hi, welcome to the Uniprot Protein Search Alexa Skill."
 * Type or say: "search brain"
  * Return: "Tachykinins. Function: Tachykinins are active peptides which excite neurons, evoke behavioral responses, are potent vasodilators and secretagogues, and contract (directly or indirectly) many smooth muscles"
 * Type or say: "search insulin"
  * Return: "Insulin-like growth factor 1 receptor. Function: Receptor tyrosine kinase which mediates actions of insulin-like growth factor 1 (IGF1)"
 * Type or say: "search insulin rats"
  * Return: "Brain-specific angiogenesis inhibitor 1-associated protein 2. Function: Adapter protein that links membrane-bound small G-proteins to cytoplasmic effector proteins"
