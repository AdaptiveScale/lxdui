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
    init: function(){
        console.log('Profiles init');
        this.dataTable = $('#tableProfiles').DataTable(this.tableSettings);
        $('#buttonRefresh').on('click', $.proxy(this.refreshProfiles, this));

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
        $('#tbl-profile').DataTable().clear();
        $('#tbl-profile').DataTable().destroy();
        $('#tbl-profile').DataTable({
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
                               '<h4>'+name+'</h4>'+
                                    Object.keys(field[name]).map((prop)=>{
                                        return '<li>'+prop+':'+field[name][prop]+'</li>'
                                    }).join('')+
                               '</ul>'
                            }).join('');
                    }
                },
                { data : "used_by" },
            ]
        });
    }
}