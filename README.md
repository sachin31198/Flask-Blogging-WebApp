# Flask-Blogging-WebApp

Database schema

Posts
  PostID (identity)
  PostTitle (varchar)
  PostDate (datetime)
  Deleted (int)
  OwnerID (int FK to Users)

PostDetails
  PostDetailID (identity)
  PostID (FK to Posts)
  Sequence (int) -> for long posts you order by this
  PostText (text)

Comments
  CommentID (identity)
  Comment (text)
  CommenterID (int FK to Users)
  CommentDate (datetime)
  Deleted (int)

Users
  UserID (identity)
  UserNAme (varchar)
  UserEmail (varchar)
  CreatedDate (datetime)
  Active (int)
