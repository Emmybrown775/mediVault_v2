let count = 0;

function newFile() {
    if (count === 0) {
        const newFile = document.createElement("div")
        newFile.innerHTML = `
        <form class="list-group-item"
                                          action="{{ url_for("patient", patient_id=patient.id) }}" method="post"
                                          enctype="multipart/form-data">
                                        <input name="form" type="hidden" value="file">
                                        <input name="file" class="" type="file">
                                        <div class="float-right">
                                            <button type="submit" class="btn btn-dark-red-f btn-sm">
                                                <i class="las la-file-medical"></i>add
                                            </button>
                                        </div>
                                    </form>
        `
        document.getElementById("medical_records").append(newFile)

        count += 1
    }}

function makeInputsEditable() {
    const inputs = document.querySelectorAll('.form-control');
    inputs.forEach((input) => {
        if (input.type !== 'date' || input.id !== "reg-date") {
            if (input.id !== "uuid"){
                input.readOnly = false;
            }

        }
    });

    const selects = document.querySelectorAll('select.form-control');
    selects.forEach((select) => {
        select.disabled = false;
    });

    const submitButton = document.getElementById('submitButton');
    submitButton.style.display = 'block';

}