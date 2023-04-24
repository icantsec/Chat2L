var globalIDCounter = 0;
var questions = []


	//get the container that all the questions/answers are stored in
    var qContainers = document.getElementsByClassName("d2l-quiz-question-autosave-container");
    console.log("qcontainers: " + qContainers.length)
    console.log(qContainers);
	//loop through every answer/question combo container to extract this information
    for(var idx = 0; idx < qContainers.length; idx++) {
        var currContainer = qContainers[idx];
        var getLabels = true;
        var html_blocks = currContainer.getElementsByTagName("d2l-html-block");
        if(html_blocks.length == 0) {
            continue;
        }

        var element = html_blocks[0];

		//if there is no ID assigned to the element, we will add a custom one so we can keep track of it
        if(element.id.length == 0) {
			element.id = "eleUUID" + globalIDCounter;
			globalIDCounter++;
        }
        var questionID = element.id;

		//remove the tags from the questions/answers
        var text = html_blocks[0].html;
        text = text.replace("<p>", "");
        text = text.replace("</p>", "");
        text = text.replace("\\n", " ");

		//create our question object
        currQuestion = {
            "question": {
                "id": questionID,
                "text": text
            },
            "answers": []
        }

		//if there is more than one d2l-html-block, the answers will not be in labels, and we can loop through them to get all answer choices
        if(html_blocks.length > 1) {
            getLabels = false;
            for(var x = 1; x < html_blocks.length; x++) {
                currAnswer = html_blocks[x];
                var text = currAnswer.html;
                text = text.replace("<p>", "");
                text = text.replace("</p>", "");
                text = text.replace("\\n", " ");
                var ele = currAnswer;
                if(ele.id.length > 0) {
                } else {
                    ele.id = "eleUUID" + globalIDCounter;
                    globalIDCounter++;
                }

                answerObj = {
                    "id": ele.id,
                    "text": text
                }
                currQuestion["answers"].push(answerObj);
            }
        }

        //otherwise we will need to get them from the labels
        if(getLabels) {
            //get all labels
            var label_blocks = currContainer.getElementsByTagName("label");
            //if they exist we can continue to process them
            if(label_blocks != undefined && label_blocks.length > 0) {
                for(var x = 0; x < label_blocks.length; x++) {
                    var currAnswer = label_blocks[x];
                    if(currAnswer.childElementCount == 0 && currAnswer.innerHTML.length > 0) {
                        var text = currAnswer.innerHTML;
                        text = text.replace("<p>", "");
                        text = text.replace("</p>", "");
                        text = text.replace("\\n", " ");
                        var cA = currAnswer;
                        if(cA.id.length > 0) {
                        } else {
                            cA.id = "eleUUID" + globalIDCounter;
                            globalIDCounter++;
                        }
                        answerObj = {
                            "id": cA.id,
                            "text": text
                        }
                        currQuestion["answers"].push(answerObj);
                    }
                }
            }


        }

        //add this question/answer set to the outer array
        questions.push(currQuestion);
    }


//return our nice little array to our python overlord for processing
return JSON.stringify(questions);
