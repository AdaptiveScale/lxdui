function showCreateContainer()
{
    var html = '';
    HTML.set('set-div', 'cmp-create-container', function (response) {
        for(var i = 0; i <= selectedImages.length - 1; i++)
        {
            html += `<div class="panel panel-default">`
                        + `<div class="panel-heading" role="tab" id="headingOne">`
                        + `<h4 class="panel-title">`
                                + `<a role="button" data-toggle="collapse" data-parent="#accordion" href="#${i}" aria-expanded="true" aria-controls="collapseOne"> <span id="description"></span>`
                                +`<span id="${selectedImages[i]}">`+display_img_names[i]+` <label class="nrOfNodes_${i} pull-right">1 Node</label></span>`
                                + `</a>`
                            + `</h4>`
                        + `</div>`
                        + `<div id="${i}" class="panel-collapse collapse in" role="tabpanel" aria-labelledby="${i}">`
                            +`<div class="panel-body">`
                                +`<div class="form-group">`
                                    + `<label class="col-sm-4 control-label">Container Name</label>`
                                    + `<label class="col-sm-3 control-label">Number</label>`
                                    + `<div class="clearfix"></div>`
                                    +  `<div class="col-sm-4">`
                                        +`<input type="text" class="containerName form-control" value="cnt-" placeholder="container name prefix" required/>`
                                    + `</div>`
                                    +  `<div class="col-sm-3">`
                                        +`<input type="number" class="cntNrs form-control" min="1" value="1" onchange="changeNumberOfContainers(${i}, $(this))" style="width:60px">`
                                    + `</div>`
                                +`</div>`
                                +`</div>`
                                +`<input class="img_alias" type="hidden" value="${selectedImages[i]}">`
                            +`</div>`
                        +`</div>`
                    +`</div>`
                    + `<!-------- endline ----------!>`;
        }
        $('#accordion').html(html);
    })
}