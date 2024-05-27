window.onload = () => {
    let params = new URLSearchParams(window.location.search);
    let name = params.get('name')
    let offer = params.get('offer')
    let tech = params.get("technology")

    if (name) {document.querySelector("#name").value = name;}

    if (offer) {
        let offer_option = Array.from(
            document.querySelectorAll(".offer__option")
        ).find(el => el.textContent.includes(offer));
        if (offer_option) {offer_option.selected = true;}
    } else {
        document.querySelector(".offer__option").selected = true;
    }

    if (tech) {
        let tech_option = Array.from(
            document.querySelectorAll(".tech__option")
        ).find(el => el.textContent.includes(tech));
        if (tech_option) {tech_option.selected = true;}
    } else {
        document.querySelector(".tech__option").selected = true;
    }

}