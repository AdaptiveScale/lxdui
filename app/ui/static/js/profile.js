App.profiles = App.profiles || {
    data:[],
    error:false,
    errorMessage:'',
    loading:false,
    initiated:false,
    tableSettings: {
        rowId:'name',
        searching:true,
        responsive: true,
        select: true,
        columnDefs: [
            {
                orderable: false,
                className: 'select-checkbox',
                targets:   0
            }
        ],
        select: {
            style:    'multi',
            selector: 'td:first-child'
        },
        order: [[ 1, 'asc' ]],
    },
    configEditor:null,
    devicesEditor:null,

    init: function(){
        console.log('Profiles init');
        this.configEditor = ace.edit('configEditor');
        this.devicesEditor = ace.edit('devicesEditor');
        this.configEditor.session.setMode('ace/mode/json');
        this.devicesEditor.session.setMode('ace/mode/json');
        this.dataTable = $('#tableProfiles').DataTable(this.tableSettings);
        $('#buttonNewProfile').on('click', $.proxy(this.showNewProfile, this));
        $('#backProfile').on('click', $.proxy(this.backToProfiles, this));
        $('#buttonCreateProfile').on('click', $.proxy(this.createProfile, this));
        $('#buttonDeleteProfile').on('click', $.proxy(this.deleteProfile, this));
        App.setActiveLink('profile');
        this.getData();
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
    getData: function(){
        this.setLoading(true);
        $.get(App.baseAPI+'profile', $.proxy(this.getDataSuccess, this));
    },
    getDataSuccess: function(response){
        console.log('success', response.data);
        this.setLoading(false);
        this.data = response.data;
        if(!this.initiated)
            return this.initiated = true;

        this.updateLocalTable(response.data);
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
    },
    backToProfiles: function() {
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
}