function filterTable() {
  let filterPassport = document.getElementById("filter-passport").value.toUpperCase();
  let filterFirstName = document.getElementById("filter-first-name").value.toUpperCase();
  let filterLastName = document.getElementById("filter-last-name").value.toUpperCase();
  let filterEmail = document.getElementById("filter-email").value.toUpperCase();
  let filterPhone = document.getElementById("filter-phone").value.toUpperCase();
  let filterCity = document.getElementById("filter-city").value.toUpperCase();
  let filterAddress = document.getElementById("filter-address").value.toUpperCase();
  let filterZipcode = document.getElementById("filter-zipcode").value.toUpperCase();

  let tableRows = document.querySelectorAll("#row");

  for (let i = 0; i < tableRows.length; i++) {
    let row = tableRows[i];
    let passport = row.getElementsByTagName("td")[0].textContent.toUpperCase();
    let firstName = row.getElementsByTagName("td")[1].textContent.toUpperCase();
    let lastName = row.getElementsByTagName("td")[2].textContent.toUpperCase();
    let email = row.getElementsByTagName("td")[3].textContent.toUpperCase();
    let phone = row.getElementsByTagName("td")[4].textContent.toUpperCase();
    let city = row.getElementsByTagName("td")[5].textContent.toUpperCase();
    let address = row.getElementsByTagName("td")[6].textContent.toUpperCase();
    let zipcode = row.getElementsByTagName("td")[7].textContent.toUpperCase();

    if (
      passport.indexOf(filterPassport) > -1 &&
      firstName.indexOf(filterFirstName) > -1 &&
      lastName.indexOf(filterLastName) > -1 &&
      email.indexOf(filterEmail) > -1 &&
      phone.indexOf(filterPhone) > -1 &&
      city.indexOf(filterCity) > -1 &&
      address.indexOf(filterAddress) > -1 &&
      zipcode.indexOf(filterZipcode) > -1
    ) {
      row.style.display = "";
    } else {
      row.style.display = "none";
    }
  }
}
