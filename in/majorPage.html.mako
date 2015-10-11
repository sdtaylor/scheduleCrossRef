<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="description" content="">
        <meta name="author" content="">
        <title>Simpler UF Grad Student Schedule</title>
        <!-- Bootstrap core CSS + datables integration -->
        <link rel="stylesheet" type="text/css" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.css">
        <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.9/css/dataTables.bootstrap.min.css">
        <!-- Custom styles for this template -->
        <link href="index.css" rel="stylesheet">
        <!-- JS libraries for bootstrap and datatables -->
	<script type="text/javascript" language="javascript" src="http://code.jquery.com/jquery-1.11.3.min.js"></script>
	<script type="text/javascript" language="javascript" src="https://cdn.datatables.net/1.10.9/js/jquery.dataTables.min.js"></script>
	<script type="text/javascript" language="javascript" src="https://cdn.datatables.net/1.10.9/js/dataTables.bootstrap.min.js"></script>
        <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
        <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
      <script src="https://oss.maxcdn.com/libs/respond.js/1.3.0/respond.min.js"></script>
    <![endif]-->
	<script type="text/javascript" class="init">

/* Formatting function for row details - modify as you need */
function format ( d ) {
    // `d` is the original data object for the row
    return '<table cellpadding="20" cellspacing="10" border="0" style="padding-left:150px;">'+
	    '<col width="100px" />'+
	    '<col width="100px" />'+
	    '<col width="100px" />'+
	    '<col width="100px" />'+
	    '<col width="100px" />'+
	    '<col width="500px" />'+
        '<tr>'+
            '<td></td>'+
	    '<td><span style="text-decoration:underline;">Fee</span></td>'+
	    '<td><span style="text-decoration:underline;">Days</span></td>'+
	    '<td><span style="text-decoration:underline;">Periods</span></td>'+
	    '<td><span style="text-decoration:underline;">Where</span></td>'+
	    '<td><span style="text-decoration:underline;">Last Offered</span></td>'+
        '</tr>'+
        '<tr>'+
            '<td></td>'+
            '<td>'+d.fee+'</td>'+
            '<td>'+d.days+'</td>'+
            '<td>'+d.times+'</td>'+
	    '<td>'+d.building+' '+d.room+'</td>'+
	    '<td>'+d.lastSeen+'</td>'+
        '</tr>'+
    '</table>';
}

$(document).ready(function() {
    var table = $('#maintable').DataTable( {
	"paging": false,
	"info": false,
	"ajax": "${thisMajor['name']}objects.txt",
        "columns": [
            {
                "className":      'details-control',
                "orderable":      false,
                "data":           null,
                "width":           "5%",
                "defaultContent": ''
            },
	{ "data" :"coursePrefix"},
	{ "data": "courseNum"},
	{ "data": "section"},
	{ "data": "credits"},
	{ "data": "title"},
	{ "data": "prof"},
	{ "data": "frequency"}
        ],
        "order": [[1, 'asc']]
    } );
     
    // Add event listener for opening and closing details
    $('#maintable').on('click', 'td.details-control', function () {
        var tr = $(this).closest('tr');
        var row = table.row( tr );
 
        if ( row.child.isShown() ) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
        }
        else {
            // Open this row
            row.child( format(row.data()) ).show();
            tr.addClass('shown');
        }
    } );
} );


	</script>
    </head>
    <body>
        <div class="container">
            <!-- Static navbar -->
            <div class="navbar navbar-default" role="navigation">
                <div class="navbar-header">
                    <a class="navbar-brand" href="#" style="display: block;">A Simple UF Grad Student Schedule</a>
                </div>
                <div class="navbar-collapse collapse">
                    <ul class="nav navbar-nav" style="display: block;">
                        <li class="active">
                            <a href="index.html">Home</a>
                        </li>
                    </ul>
                    <a class="navbar-brand navbar-right" href="#" style="display: block;"><b>${thisMajor['name']} Spring 2016</b></a>
                </div>
                <!--/.nav-collapse -->
            </div>
            <!-- Main component for a primary marketing message or call to action -->
            <div class="container">
                <table id="maintable" class="table"> 
                    <thead>
                        <tr>
                            <th></th>
                            <th>Dept</th>
                            <th>Number</th>
                            <th>Section</th>
                            <th>Credits</th>
                            <th>Name</th>
                            <th>Professors</th>
                            <th>Frequency</th>
                        </tr>
                    </thead>
                </table>
            </div>
        </div>         
        <!-- /container -->
        <!-- Bootstrap core JavaScript
    ================================================== -->
    </body>
</html>

