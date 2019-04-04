(function() {

  //handle radio inputs on the page...
  var group = document.getElementsByClassName("js-clientform__radiogroup")[0];
  group.onclick = function(e) {
    ToggleRadioAttributes(e);
  }
  group.onkeydown = function(e) {
    RadioKeyboardSupport(e, ToggleRadioAttributes);
  }
  function ToggleRadioAttributes(e) { //sets aria, class and index based on active element
    var radioButtons = e.target.parentNode.children;
    for(var i = 0; i < radioButtons.length; i++) {
      var x = radioButtons[i];
      selStyle = x.className.split(" ")[0] + "--selected";
      if(x == document.activeElement) {
        x.setAttribute("tabindex", "0");
        x.setAttribute("aria-checked", "true");
        x.classList.add(selStyle);
      }
      else {
        x.setAttribute("tabindex", "-1");
        x.setAttribute("aria-checked", "false");
        x.classList.remove(selStyle);
      }
    }
  }
  function RadioKeyboardSupport(e, cbck) { //handles up down and space keys
    var a = document.activeElement;
    if(a) {
      var role = a.getAttribute("role");
      if( role && (role == "radio") ) {
        var group = e.target.parentNode;
        var children = group.children;
        var k = e.keyCode;
        if( k == 38 || k == 40 ) {
          e.preventDefault();
          var curr;
          for(var i = 0; i < children.length; i++) {
            if( a == children[i] ) {
              curr = i;
            }
          }
          if( k == 38 ) {
            if( curr - 1 >= 0 ) {
              children[curr - 1].focus();
              e.preventDefault();
              cbck(e);
            }
          }
          else if( k == 40 ) {
            if( curr + 1 < children.length ) {
              children[curr + 1].focus();
              e.preventDefault();
              cbck(e);
            }
          }
        }
        if( k == 32 ) {
          e.preventDefault();
          cbck(e);
        }
      }
    }
  } //END radio input handler



  //handle the submit button on the page...
  var gate = true;
  document.getElementsByClassName("js-clientform__button")[0].onclick = function() {
    var d = ValidateClientForm();
    if(d && gate) {
      gate = false;
      var over = document.getElementsByClassName("clientform__overlay")[0];
      over.style.display = "inherit";
      $.ajax({
        url : "/Response",
        type : 'POST',
        data : d,
        complete: function() {
          gate = true;
          over.style.display = "none";
        },
        success: function(response) {
          var obj = JSON.parse(response);
          var msg = "" + obj.surveyLink;
          FlashMessage(msg);
        },
        error: function(error) {
          console.log(error);
        }
      });
    }
  } //END submit handler



  //validates the form and if success returns the JSON data...
  function ValidateClientForm() {
    var data = {};
    var success = true;
    var input1 = document.getElementById("rdg1"); //validates the radio group
    var addClass1 = "clientform__radiogroup--error";
    var errorArea1 = document.getElementById("err1");
    var node1 = CreateErrorMessage("Vestibulum massa libero");
    if(document.getElementsByClassName("clientform__radio--selected").length != 1) { //error conditions
      success = false;
      ToggleError(input1, addClass1, errorArea1, node1, true);
    }
    else {
      data.options = document.getElementsByClassName("clientform__radio--selected")[0].getAttribute("data-options");
      ToggleError(input1, addClass1, errorArea1, node1, false);
    }
    var input2 = document.getElementById("txt1"); //validates the input box
    var addClass2 = "clientform__text--error";
    var errorArea2 = document.getElementById("err2");
    var node2 = CreateErrorMessage("Nullam semper purus rhoncus tortor faucibus");
    if(input2.value == "") { //error conditions
      success = false;
      ToggleError(input2, addClass2, errorArea2, node2, true);
    }
    else {
      data.email = input2.value;
      ToggleError(input2, addClass2, errorArea2, node2, false);
    }
    if(success) {
      return data;
    }
    else {
      return null;
    }
    function ToggleError(input, classname, errorarea, errormsg, flag) { //add or remove aria and class
      if(flag == true) {
        input.classList.add(classname);
        input.setAttribute("aria-invalid", "true");
        input.setAttribute("aria-describedby", errorarea.id);
        if(!errorarea.hasChildNodes()) {
          errorarea.append(errormsg);
        }
      }
      else {
        input.classList.remove(classname);
        input.removeAttribute("aria-invalid");
        input.removeAttribute("aria-describedby");
        if(errorarea.hasChildNodes()) {
          var node = errorarea.children[0];
          errorarea.removeChild(node);
        }
      }
    }
    function CreateErrorMessage(msg) { //create a simple text node with the error message
      var node = document.createElement("p");
      var txt = document.createTextNode(msg);
      node.appendChild(txt);
      node.classList.add("section__message--error");
      node.setAttribute("role", "alert");
      return node;
    }
  } //END validate form function



  //show and then hide the toaster window on the page...
  function FlashMessage(msg) {
    var toast = document.getElementById("toaster");
    toast.innerHTML = msg;
    toast.classList.add("toaster--show");
    setTimeout(function() { //show it for 6 seconds
      toast.innerHTML = "";
      toast.classList.remove("toaster--show");
    }, 8000);
  } //END flash function



  FlashMessage(document.getElementById("toaster").innerHTML); //show the toaster on load for GET survey description

})();
