App.profiles = App.profiles || {
    data:[],
    error:false,
    errorMessage:'',
    loading:false,
    initiated:false,
    activeProfile: {},
    tableSettings: {
        rowId:'name',
        searching:true,
        responsive: false,
        select: true,
        scrollX: true,
        columnDefs: [
            {
                orderable: false,
                className: 'select-checkbox',
                targets:   0
            }
        ],
         dom: "<'tbl-header'<'row'<'col-sm-4 text-left'f><'col-sm-2 refresh-list-place'><'col-sm-6 json-place'>>>" +
        "<'row'<'col-sm-12'tr>>" +
        "<'row'<'col-sm-4'i><'col-sm-2 text-right'l><'col-sm-6 text-right'p>>",
        "oLanguage": {
          "sLengthMenu": "List _MENU_ ",
        },
        select: {
            style:    'multi',
            selector: 'td:first-child'
        },
        order: [[ 1, 'asc' ]],
        initComplete: function(settings, json) {
            var tempButton = $('.rawJSONProfiles').clone();
            tempButton.removeClass('rawJSONProfiles');
            tempButton.on('click', $.proxy(App.profiles.showJSON, App.profiles));
//            $('#'+$(this).closest('table').attr('id')+'_filter').prepend(tempButton);
            $('.json-place').append(tempButton);
            tempButton.show();
        },
    },
    configEditor:null,
    devicesEditor:null,
    rawJson:null,
    init: function(){
        console.log('Profiles init');
        this.configEditor = ace.edit('configEditor');
        this.devicesEditor = ace.edit('devicesEditor');
        this.configEditor.session.setMode('ace/mode/json');
        this.devicesEditor.session.setMode('ace/mode/json');
        this.rawJson = ace.edit('rawJson');
        this.rawJson.session.setMode('ace/mode/json');
        this.rawJson.setOptions({readOnly: true});
        this.dataTable = $('#tableProfiles').DataTable(this.tableSettings);
        $('#buttonNewProfile').on('click', $.proxy(this.showNewProfile, this));
        $('#backProfile').on('click', $.proxy(this.backToProfiles, this));
        $('#buttonCreateProfile').on('click', $.proxy(this.createProfile, this));
        $('#buttonUpdateProfile').on('click', $.proxy(this.updateProfile, this));
        $('#buttonDeleteProfile').on('click', $.proxy(this.deleteProfile, this));
        $('#selectAllProfiles').on('change', $.proxy(this.toggleSelectAll, this, 'Remote'));
        this.dataTable.on('select', $.proxy(this.onItemSelectChange, this));
        this.dataTable.on('deselect', $.proxy(this.onItemSelectChange, this));
        App.setActiveLink('profile');
        this.getData();
        $('#profileForm > ul > li:nth-child(1)').addClass('active');
    },
    refreshProfiles: function(e){
        console.log('refreshProfiles');
        e.preventDefault();
        console.log('dataTable', this.dataTable);
        this.getData();
    },
    setLoading: function(state){
        this.loading=true;
    },
    getProfile: function(name){
        return $.get(App.baseAPI+'profile/'+name, $.proxy(this.getProfileDataSuccess, this));
    },
    getProfileDataSuccess: function(response) {
        this.activeProfile = response.data;

        $('#name').val(this.activeProfile.name);
        this.configEditor.setValue(JSON.stringify(this.activeProfile.config, null , '\t'));
        this.devicesEditor.setValue(JSON.stringify(this.activeProfile.devices, null , '\t'));
    },
    getData: function(){
        this.setLoading(true);
        $.get(App.baseAPI+'profile', $.proxy(this.getDataSuccess, this));
    },
    getDataSuccess: function(response){
        this.setLoading(false);
        this.data = response.data;
        if(!this.initiated)
            return this.initiated = true;

        this.rawJson.setValue(JSON.stringify(response.data, null , '\t'));
        //this.updateLocalTable(response.data);
    },
    showJSON: function(e) {
        this.rawJson.setValue('');
        $('.modal-title').text('');
        $('.modal-title').text('RAW JSON for Profiles');
        $('.modal-title').append(' <span class="glyphicon glyphicon-refresh spinning loader">');
        $("#jsonModal").modal("show");

        this.getData();

    },
    showUpdateProfile: function(elem) {
        this.getProfile(elem);

        $('#newProfile').show();
        $('#profileList').hide();
        $('#buttonUpdateProfile').show();
        $('#buttonCreateProfile').hide();
    },
    updateLocalTable: function(jsonData){
        this.data = jsonData;
        $('#tableProfiles').DataTable().clear();
        $('#tableProfiles').DataTable().destroy();
        $('#tableProfiles').DataTable({
            searching:true,
            data : this.data,
            responsive: true,
            columns : [
                {
                    data : null,
                    defaultContent:'<input type="checkbox" class="profiles-check">'
                },
                { data : "name" },
                { data : "description"},
                { data : "devices",  render: function(field){
                    return Object.keys(field).map((name)=>{
                               return '<ul>'+
                               '<h5>'+name+'</h5>'+
                                    Object.keys(field[name]).map((prop)=>{
                                        return '<li>'+prop+':'+field[name][prop]+'</li>'
                                    }).join('')+
                               '</ul>'
                            }).join('');
                    }
                },
                { data : 'used_by' },
            ]
        });
    },
    showNewProfile: function() {
        $('#newProfile').show();
        $('#profileList').hide();

        $('#buttonUpdateProfile').hide();
        $('#buttonCreateProfile').show();
    },
    backToProfiles: function() {
        $('#profileForm').trigger('reset');
        this.configEditor.setValue('');
        this.devicesEditor.setValue('');
        $('#newProfile').hide();
        $('#profileList').show();
    },
    createProfile: function() {
        console.log('Create Profile...');
        if (this.configEditor.getValue() === '') {
            configValue = {};
        }
        else {
            configValue = JSON.parse(this.configEditor.getValue());
        }
        if (this.devicesEditor.getValue() === '') {
            devicesValue = {};
        }
        else {
            devicesValue = JSON.parse(this.devicesEditor.getValue());
        }

        $.ajax({
            url:App.baseAPI+'profile/',
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify({
                name: $('#name').val(),
                config: configValue,
                devices: devicesValue,
            }),
            success: $.proxy(this.onProfileCreate, this)
        });
    },
    onProfileCreate: function(response) {
        console.log(response);
        console.log('updateSuccess:', 'TODO - add alert and refresh local data');
    },
    updateProfile: function() {
        console.log('Update Profile...');
        if (this.configEditor.getValue() === '') {
            configValue = {};
        }
        else {
            configValue = JSON.parse(this.configEditor.getValue());
        }
        if (this.devicesEditor.getValue() === '') {
            devicesValue = {};
        }
        else {
            devicesValue = JSON.parse(this.devicesEditor.getValue());
        }

        $.ajax({
            url:App.baseAPI+'profile/' + this.activeProfile.name,
            type: 'PUT',
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify({
                new_name: $('#name').val(),
                config: configValue,
                devices: devicesValue,
            }),
            success: $.proxy(this.onProfileUpdate, this)
        });
    },
    onProfileUpdate: function(response) {
        console.log(response);
        console.log('updateSuccess:', 'TODO - add alert and refresh local data');
    },
    deleteProfile: function() {
        this.dataTable.rows( { selected: true } ).data().map(function(row){
            $.ajax({
                url: App.baseAPI+'profile/' + row['name'],
                type: 'DELETE',
                success: $.proxy(this.onDeleteSuccess, this, row['name'])
            });
        }.bind(this));
    },
    onDeleteSuccess: function(name){
        this.dataTable.row("#"+name).remove().draw();
        $('.success-msg').text('Profile ' + name + ' has been removed');
        var parent = $('.success-msg').parent().toggleClass('hidden');

        setTimeout(function(){
          parent.toggleClass('hidden');
        }, 10000);
    },
    toggleSelectAll:function(name, event){
        if(event.target.checked){
            this.dataTable.rows().select();
        }else{
            this.dataTable.rows().deselect();
        }
    },
    onItemSelectChange : function(e, dt, type, indexes ){
    console.log('argumentss', arguments);
        var state = this.dataTable.rows({selected:true}).count()>0;
        console.log('newState', state);
        $('#selectAllProfiles').prop('checked', this.dataTable.rows({selected:true}).count()==this.dataTable.rows().count());
        var buttonStates = state?'removeAttr':'attr';
        $('#buttonDeleteProfile')[buttonStates]('disabled','disabled');
    }
}