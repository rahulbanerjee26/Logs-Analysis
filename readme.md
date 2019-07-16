
<h1> Log Analysis </h1>

<h2> Nanodegree : Full Stack Web Developer, Udacity </h2>

  

<p><b>Used psycopg2 and psql to complete the project</b></p>

  

<h3>  <u> Task </u></h3>

<p> You've been hired onto a team working on a newspaper site. The user-facing newspaper site frontend itself, and the database behind it, are already built and running. You've been asked to build an internal reporting tool that will use information from the database to discover what kind of articles the site's readers like.

  

The database contains newspaper articles, as well as the web server log for the site. The log has a database row for each time a reader loaded a web page. Using that information, your code will answer questions about the site's user activity.

</p>

  

<h3>  <u> Software Required </u>  </h3>


<a href="https://www.virtualbox.org/wiki/Download_Old_Builds_5_1">Virtual Box</a>

<a href="https://www.vagrantup.com/">Vagrant </a>

<a href="https://www.python.org/downloads/"> Python </a>

<a href="https://www.postgresql.org/download/"> Postgresql </a>(Already installed in vm) 

<a href="https://git-scm.com/"> Git Bash </a>



  

<h3>  <u> Steps to Run </u>  </h3>

<ul>

<li> Install Vagrant and Virtual Box </li>

<li> Log in using vagrant ssh </li>

<li> Download <a href="https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip">udacity's files</a>. It contains the sql commands to create and initialize database</li>

<li> Clone Repo and paste content in shared folder </li>

<li> Using git bash cd to the folder </li>

<li> Create and populate the database by typing

     psql -d news -f newsdata.sql

<li> Type the following to run the program

    python solution.py  
</ul>

  

<h3><u> Views Created </u></h3>

  

    1) most_visits_path
     
		create view most_visits_path as
    
        select path,
        
        count(path) as visits from log
        
        where path like '/article/%'
        
        group by path
        
        order by visits desc;
        

    2)most_visits_title
    
	    create view most_visits_title as
    
	    select a.author,
    
	    a.title,
    
	    m.visits from articles as
    
	    a,most_visits_path as m
    
	    where a.slug = substr(m.path,10);
    
      

    3) authors_view
    
	    create view authors_view as select author as id,
    
    	sum(visits) from most_visits_title
    
    	group by author;

      
    
    4) totalRequest 
	    create view totalRequests as select date(time) as date,
    
	    count(*) as total_requests from log
    
	    group by date;
    
      
    
    5) errorRequest 
	    create view errorRequests as select date(time) as date,
    
	    count(*) as total_requests from log
    
	    where status not like '200%'
    
	    group by date;
    
      
    
    6) errorPercentage 
	    create view errorPercentage as
    
	    select to_char(a.date :: DATE, 'Mon dd, yyyy') as date,
    
	    round((b.total_requests * 100)::numeric/ 			a.total_requests,3)
    
	    as percentage from totalRequests as a, errorRequests as b
    
	    where a.date = b.date;

<h3><u> Author</u> </h3>
<b>Rahul Banerjee</b>


