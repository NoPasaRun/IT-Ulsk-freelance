window.onload = () => {
    const content_blocks = document.querySelectorAll(".accordeon__block")
    const buttons = document.querySelectorAll(".accordeon__item")
    buttons.forEach((el, index) => {
        el.addEventListener("click", () => {
            buttons.forEach((el, index) => {
                el.classList.remove("accordeon__item_active")
                content_blocks[index].classList.add("accordeon__block_hidden")
            })
            el.classList.add("accordeon__item_active")
            content_blocks[index].classList.remove("accordeon__block_hidden")
        })
    })
}