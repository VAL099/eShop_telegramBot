create table Sellers(
	id int primary key Not null IDENTITY(1,1),
	userId varchar(255),
	namee varchar(255),
	username varchar(255) not null,
	phoneNum varchar(255)
);

create table Products(
	id int primary key Not null IDENTITY(1,1),
	prodName varchar(255) not null,
	category varchar(50) not null,
	subcategory varchar(50) not null,
	sellerId int not null foreign key references Sellers(id),
	descript text,
	photo image,
	priceLabel bit,
	qualityLabel bit
);