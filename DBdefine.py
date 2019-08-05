#Import pyodbc module using below command
import pyodbc as db
 
#Create connection string to connect DBTest database with windows authentication
con = db.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER=.;Trusted_Connection=yes;DATABASE=BlogReport')
cur = con.cursor()

cur.execute("Create table users("
			"UserID int not null primary key identity,"
			"UserName varchar(255) not null,"
			"UserEmail varchar (50) not null,"
			"Password varchar (32) not null,"
			"createdDate datetime,"
			"Unique(UserEmail),"
			"Unique(UserName))"
	)
cur.execute("Create table Posts("
			"PostID int not null primary key identity,"
			"PostTitle varchar(255) not null,"
			"PostDate datetime,"
			"Deleted Bit not null,"
			"OwnerID int foreign key references users(UserID)"
			")"
	)
cur.execute("Create table PostDetails("
			"PostDetailID int not null primary key identity,"
			"PostID int foreign key references Posts(PostID),"
			"PostText text not null,"
			"Unique(PostDetailID))"
	)
cur.execute("Create table Comments("
			"CommentID int not null primary key identity,"
			"Comment text not null,"
			"CommenterID int foreign key references Users(UserID),"
			"CommentDate datetime,"
			"Deleted Bit not null,"
			"Unique(CommentID))"
	)

cur.commit() #Use this to commit the insert operation
cur.close()
con.close()
