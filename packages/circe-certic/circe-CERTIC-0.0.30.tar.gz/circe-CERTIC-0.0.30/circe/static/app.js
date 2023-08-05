class TransformationOptionWidget {
    constructor(description) {
        this.description = description;
    }

    renderTo(parent) {
        let root = document.createElement("tr");
        let title = document.createElement("td");
        title.innerText = this.description.label;
        let select_root = document.createElement("td");

        if(this.description.free_input){
            let text_input = document.createElement("input");
            text_input.setAttribute("type", "text");
            text_input.setAttribute("name", this.description.id);
            text_input.setAttribute("list", this.description.id + "_datalist");
            text_input.setAttribute("class", "opt_select");
            select_root.appendChild(text_input);
            let data_list = document.createElement("datalist");
            data_list.setAttribute("id", this.description.id + "_datalist");
            select_root.appendChild(data_list);
            for (let [key, value] of Object.entries(this.description.values)) {
                let opt = document.createElement("option");
                opt.setAttribute("value", key);
                opt.innerText = value;
                data_list.appendChild(opt);
            }
            if(this.description.default){
                text_input.value = this.description.default;
            }
        }else {
            let select = document.createElement("select");
            select.setAttribute("class", "opt_select");
            select.setAttribute("name", this.description.id);
            select_root.appendChild(select);
            for (let [key, value] of Object.entries(this.description.values)) {
                let opt = document.createElement("option");
                opt.setAttribute("value", key);
                opt.innerText = value;
                if (key === this.description.default) {
                    opt.setAttribute("selected", "selected");
                }
                select.appendChild(opt);
            }
        }
        root.appendChild(title);
        root.appendChild(select_root)
        parent.appendChild(root);
    }
}

class TransformationWidget {
    constructor(name, description) {
        this.name = name;
        this.description = description;
    }

    renderTo(parent) {
        let list_item = document.createElement("li");
        let hidden_name = document.createElement("input");
        hidden_name.setAttribute("type", "hidden");
        hidden_name.setAttribute("value", this.name);
        list_item.appendChild(hidden_name);
        let handle_bar = document.createElement("div");
        handle_bar.setAttribute("class", "dragItemHandle");
        handle_bar.innerText = this.description.label;
        list_item.appendChild(handle_bar);

        let help = document.createElement("p");
        help.innerText = this.description.help;
        list_item.appendChild(help);
        let options = document.createElement("table");
        for (let i = 0; i < this.description.options.length; i++) {
            let option = new TransformationOptionWidget(this.description.options[i]);
            option.renderTo(options);
        }
        list_item.appendChild(options);

        let remove_button = document.createElement("button");
        remove_button.setAttribute("class", "btnRemoveTransformation sosmall");
        remove_button.setAttribute("title", "supprimer");
        remove_button.innerText = "supprimer";
        remove_button.addEventListener("click", function () {
            this.parentNode.parentNode.removeChild(this.parentNode);
        });
        list_item.appendChild(remove_button);

        parent.appendChild(list_item);
    }
}

async function initUI() {
    let next_step_enabled = false;
    let response = await fetch("/transformations/", {method: "get"});
    let service_description = JSON.parse(await response.text());
    let transfos_parent = document.getElementById("chosentransfos");
    let btnAddTransfoParent = document.getElementById("transfochoices");
    for (let [transfo_name, transfo_description] of Object.entries(service_description)) {
        let btnLi = document.createElement("li");
        let btn = document.createElement("button");
        btn.innerText = transfo_description.label;
        btn.setAttribute("title", transfo_description.help);
        btn.addEventListener("click", function () {
            let transfo = new TransformationWidget(transfo_name, transfo_description);
            transfo.renderTo(transfos_parent);
        });
        btnLi.appendChild(btn);
        btnAddTransfoParent.appendChild(btnLi);

    }

    let dropzone_tpl = "<div class=\"dz-preview dz-file-preview\">\n" +
        "  <div class=\"dz-details\">\n" +
        "    <div class=\"dz-filename\"><span data-dz-name></span></div>\n" +
        "    <div class=\"dz-size\" data-dz-size></div>\n" +
        "  </div>\n" +
        "  <div class=\"dz-progress\"><span class=\"dz-upload\" data-dz-uploadprogress></span></div>\n" +
        "  <div class=\"dz-error-message\"><span data-dz-errormessage></span></div>\n" +
        "</div>\n"

    Dropzone.autoDiscover = false;
    let myDropzone = new Dropzone("#dropzone", {
        paramName: "file",
        maxFilesize: 50,
        timeout: 1000 * 60 * 30,
        dictFileTooBig: "Fichier trop volumineux ({{filesize}} mo). Taille maximale: {{maxFilesize}} mo",
        url: "/upload/",
        createImageThumbnails: false,
        previewTemplate: dropzone_tpl
    });

    myDropzone.on("complete", function (file) {
        if (!next_step_enabled) {
            if (file.status !== "error") {
                let next_step = document.getElementById("next");
                next_step.style.display = "block";
                Sortable.create(document.getElementById("chosentransfos"),
                    {"animation": 100, "handle": ".dragItemHandle"});
                next_step_enabled = true;
            }
        }
    });

    document.getElementById("btnGetFiles").addEventListener("click", async function () {
        let job = [];
        let transfos_parent = document.getElementById("chosentransfos");
        for (let i = 0; i < transfos_parent.childNodes.length; i++) {
            let transfo_node = transfos_parent.childNodes[i];
            let name_input = transfo_node.querySelector("input[type=hidden]");
            let options_selects = transfo_node.querySelectorAll(".opt_select");
            let options = {};
            for (let j = 0; j < options_selects.length; j++) {
                let select_elem = options_selects[j];
                let option_name = select_elem.getAttribute("name");
                if(select_elem.tagName === "SELECT"){
                    options[option_name] = select_elem.options[select_elem.selectedIndex].value;
                }else{
                    options[option_name] = select_elem.value;
                }
            }
            job.push({name: name_input.getAttribute("value"), options: options});
        }

        if (job.length === 0) {
            alert("Vous devez choisir au moins une conversion !");
            return;
        }

        this.disabled = true;
        this.innerText = "Fichiers en cours de conversion..."
        document.getElementById("btnGetFiles").disabled = true;

        let response = await fetch("/webui/setjob/", {
            method: "post",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(job)
        });

        if (response.status === 200) {
            document.getElementById("hidden_when_done").style.display = "none";
            document.getElementById("shown_when_done").style.display = "block";
        } else {
            alert("Le serveur a renvoyé une erreur :(");
        }

    });


}
