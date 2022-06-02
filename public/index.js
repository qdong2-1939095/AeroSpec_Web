/*
 * Author: Qingyuan Dong
 *
 * This is the javascript file to give different behaviours to index HTML page.
 * It will fetch or post device data from localhost:8080 server.
 * If user's input is correct but still cannot access data from server, a detailed
 * error information should appear.
 */
"use strict";
(function() {
    window.addEventListener("load", init);

    function init() {
        document.getElementById("uploadButton").addEventListener("click", uploadFile);
    }

    function uploadFile() {
        let myForm = document.getElementById("myForm");
        let inpFile = document.getElementById("inpFile");

        myForm.addEventListener("submit", e => {
            e.preventDefault();

            let endpoint = "/uploadFile.php";
            let formData = new FormData();

            formData.append("inpFile", inpFile.files[0]);

            fetch(endpoint, {
                method: "post",
                body: formData
            }).catch(console.log);
        });
    }
})();