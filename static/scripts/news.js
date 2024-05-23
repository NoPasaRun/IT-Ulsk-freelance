window.onload = () => {
    let params = new URLSearchParams(window.location.search);
    let parameter = params.get('theme')
    let option = Array.from(
        document.querySelectorAll(".select__item")
    ).find(el => el.textContent.includes(parameter));
    if (option) {option.selected = true;}

    let news_block = document.querySelector(".news__grid")

    document.querySelector("#filter").addEventListener("click", () => {
        $.ajax({
            url: window.location,
            method: 'post',
            dataType: 'json',
            success: function(data){
                data.data.forEach((d) => {
                     let _new = document.createElement("a")
                    _new.href = "/news-detail?link=" + d.link
                    _new.classList.add("new")
                    let image = d.image ? d.image : "/static/images/high-res-neuro.png"

                    _new.innerHTML = `
                        <div class="new__header">
                            <img src="${image}" alt="Image" class="new__image">
                            <strong class="new__title">
                                ${d.title}
                            </strong>
                        </div>
                        <div class="new__wrapper">
                            <p class="new__text">
                                ${d.description}
                            </p>
                            <div class="new__info">
                                <span class="new__tag">${d.author}</span>
                                <span class="new__date">${d.date}</span>
                            </div>
                        </div>
                    `
                    news_block.appendChild(_new)
                })
            }
        });
    })
};