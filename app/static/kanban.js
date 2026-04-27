document.querySelectorAll(".coluna").forEach(coluna => {

    new Sortable(coluna, {
        group: "kanban",
        animation: 200,
        draggable: ".card-task",
        filter: ".menu-card, .btn-menu-card",
        preventOnFilter: false,

        ghostClass: "sortable-ghost",
        chosenClass: "sortable-chosen",
        dragClass: "sortable-drag",

        forceFallback: true,
        fallbackOnBody: true,
        swapThreshold: 0.65
    });

});