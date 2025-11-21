// https://www.w3schools.com/jsref/met_table_insertrow.asp
function addNewRow(){
    var table = document.getElementByID("ingredients_table");
    var row = table.insertRow();
    var td1 = row.insertCell(0);
    var td2 = row.insertCell(1);
    var td3 = row.insertCell(2);

    td1.innerHTML = '<input type="text"class="form-control mx-auto w-auto input" placeholder="Amount" name="amount" autocomplete="off">'
}