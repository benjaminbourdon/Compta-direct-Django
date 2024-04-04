function export_data() {
    const target = document.querySelector("#generalLedgerTable");
    const table_header = target.querySelector("thead");
    let headers = [];
    let nb_cols = 0;
    for (var cell of table_header.firstElementChild.cells) {
        headers.push(cell.textContent.trim());
        nb_cols ++;
    }

    const table_body = target.querySelector("tbody");
    let current_user_id = null;
    let result = [];
    let operation = {};
    for (var line of table_body.children) {
        
        operation = {}
        if (line.childElementCount == 1) {
            if (line.textContent.trim() ) {
                current_user_id = line.textContent.trim();
            }
        } else {
            if (line.dataset.id && current_user_id) {
                for (i=0;i<nb_cols;i++) {
                    key = headers[i];
                    value = line.cells[i].textContent.trim();
                    operation[key] = value ;
                }
                operation["entity_id"] = line.dataset.id
                operation.user_id = current_user_id
                result.push(operation);
            }
        }
    }

    console.log(result);

    const json = JSON.stringify(result);
    console.log(json);
}