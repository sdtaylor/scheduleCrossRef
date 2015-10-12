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
                    <a class="navbar-brand navbar-right" href="#" style="display: block;"><b>Spring 2016</b></a>
                </div>
            </div>
            <!-- Main section -->
        </div>
        <div class="container">
            <div class="jumbotron"> 
                <p style="display: block;">I made this to help look for classes that actually match my major. The class lists are classes for this semester that are cross referenced to a curriculum list for a particular major.</p>
                <dl style="display: block;"> 
                    <dt style="display: block;">Some notes</dt> 
                    <dd style="display: block;">
                        <ul data-pg-collapsed=""> 
			    <li>I pulled the major curriculum off their respective websites. Like the SNRE curriculum page, and the WEC grad student handbook. </li>
                            <li>Special Topic classes share a common course number (like ZOO 6927), so are annoying to cross rerference. So every special topic class will be listed for a department and be marked with Special Topic:Yes in the info. They may not be on the official curriculum, but most are fair game anyway if you petition to take it.</li>                             
			    <li>Frequency searches for the class title in the historic scheduels from the past few years. It may be off if the title has changed. </li>
                        </ul>
                    </dd>                     
                </dl>
                <h3 style="display: block;">Majors</h3>
                <ul style="display: block;"> 
% for thisMajor in majors:
                    <li style="display: list-item;" class="majorList">
                        <a href="${thisMajor['name']}.html">${thisMajor['name']}</a>
                    </li>                     
% endfor
                </ul>
            </div>
        </div>         
        <!-- /container -->
    </body>
    <footer>
            <script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
     (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
       m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
         })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-68612086-1', 'auto');
    ga('send', 'pageview');

            </script>
    </footer>

</html>
