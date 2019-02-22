<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="description" content="">
        <meta name="author" content="">
        <title>Simple UF Grad Student Schedule</title>
        <!-- Bootstrap core CSS + datables integration -->
        <link rel="stylesheet" type="text/css" href="/schedule/static/bootstrap.min.css">
        <link rel="stylesheet" type="text/css" href="/schedule/static/dataTables.bootstrap.min.css">
        <!-- Custom styles for this template -->
        <link href="index.css" rel="stylesheet">
        <!-- JS libraries for bootstrap and datatables -->
        <script type="text/javascript" language="javascript" src="/schedule/static/jquery-1.11.3.min.js"></script>
        <script type="text/javascript" language="javascript" src="/schedule/static/jquery.dataTables.min.js"></script>
        <script type="text/javascript" language="javascript" src="/schedule/static/dataTables.bootstrap.min.js"></script>
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
                    <a class="navbar-brand navbar-right" href="#" style="display: block;"></a>
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
                            <li>Special Topic classes share a common course number (like ZOO 6927), so are very annoying to cross rerference. They are marked with Special Topic:Yes in the info and won't have the categories listed. But most are fair game anyway if you petition to take it.</li>                             
                <li>All classes from relevent depts like BOT, ZOO, and  WIS are listed.</li>
			    <li>The frequency column searches for the class title in the historic schedules from the past few years. It may be off if the class title has changed. </li>
                        </ul>
                    </dd>                     
                </dl>
                <h3 style="display: block;">Majors</h3>
                <ul style="display: block;"> 
% for thisPage in pages:
                    <li style="display: list-item;" class="majorList">
                        <a href="${thisPage['link']}">${thisPage['majorName']} - ${thisPage['termPrettyName']}</a>
                    </li>                     
% endfor
                </ul>
            </div>
<%! import datetime %>
            <div>
              <dt style="display: block;">Last updated: ${datetime.datetime.now().strftime('%b %d, %Y')}</dt> 
            </div>
        </div>         
        <!-- /container -->
    </body>
    <footer>
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=UA-68612086-2"></script>
        <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());

        gtag('config', 'UA-68612086-2');
        </script>

    </footer>

</html>
