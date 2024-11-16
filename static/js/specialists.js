let count = 0;

function newSpecialists() {
    if (count === 0){
        const newSpecialist = document.createElement("tr")
        newSpecialist.innerHTML =
        `
            
            <td>
                <input type="text" name="name">
       
            </td>
            <td class="text-muted">
                <select name="gender">
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                </select>
            </td>
            <td>
                <select name="speciality">
    <option value="Cardiology">Cardiology</option>
    <option value="Dermatology">Dermatology</option>
    <option value="Endocrinology">Endocrinology</option>
    <option value="Gastroenterology">Gastroenterology</option>
    <option value="General Surgery">General Surgery</option>
    <option value="Gynecology">Gynecology</option>
    <option value="Hematology">Hematology</option>
    <option value="Neurology">Neurology</option>
    <option value="Neurosurgery">Neurosurgery</option>
    <option value="Oncology">Oncology</option>
    <option value="Orthopedics">Orthopedics</option>
    <option value="Otolaryngology (ENT)">Otolaryngology (ENT)</option>
    <option value="Pediatrics">Pediatrics</option>
    <option value="Psychiatry">Psychiatry</option>
    <option value="Pulmonology">Pulmonology</option>
    <option value="Radiology">Radiology</option>
    <option value="Rheumatology">Rheumatology</option>
    <option value="Urology">Urology</option>
    <option value="Emergency Medicine">Emergency Medicine</option>
    <option value="Family Medicine">Family Medicine</option>
    <option value="Nephrology">Nephrology</option>
    <option value="Plastic Surgery">Plastic Surgery</option>
    <option value="Anesthesiology">Anesthesiology</option>
    <option value="Infectious Diseases">Infectious Diseases</option>
    <option value="Pathology">Pathology</option>
</select>

            </td>
            <td class="text-lowercase text-muted">
                <input name="email" type="email"/>
            </td>
            <td>
                <input name="phone_number" type="number"/>
            </td>
            <td class="text-muted">
                <a href=""></a>
            </td>
            <td>
                <button type="submit" class="btn btn-sm btn-dark-red-f">Save</button>
            </td>
            <td>
                <a href=""><i class="las la-ellipsis-h"></i></a>
            </td>
        `
        document.getElementById("table-body").append(newSpecialist)

        count += 1
    }
}