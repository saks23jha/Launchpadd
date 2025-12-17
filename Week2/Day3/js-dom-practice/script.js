const titles = document.querySelectorAll(".title");

titles.forEach((title) => {
  title.addEventListener("click", () => {
    const item = title.parentElement;
    const icon = title.querySelector(".icon");

    document.querySelectorAll(".item").forEach((i) => {
      if (i !== item) {
        i.classList.remove("active");
        const ic = i.querySelector(".icon");
        if (ic) ic.textContent = "+";
      }
    });

    
    item.classList.toggle("active");
    icon.textContent = item.classList.contains("active") ? "−" : "+";
  });
});
