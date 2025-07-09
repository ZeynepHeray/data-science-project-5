import psycopg2

## Bu değeri localinde çalışırken kendi passwordün yap. Ama kodu pushlarken 'postgres' olarak bırak.
password = 'postgres'

def connect_db():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        database="postgres",
        user="postgres",
        password=password
    )

# 1- Null emailleri 'unknown@example.com' ile değiştir
def clean_null_emails():
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""select coalesce(c.email,'unknown@example.com') from cw5.customers as c""")
            conn.commit()

# 2- Hatalı emailleri bul
def find_invalid_emails():
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""select c.email from cw5.customers as c where strpos(c.email, '@')=0""")
            return cur.fetchall()

# 3- İsimlerin ilk 3 harfi
def get_first_3_letters_of_names():
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""select c.full_name ,left(c.full_name,3)as short_name from cw5.customers as c""")
            return cur.fetchall()

# 4- Email domainlerini bul
def get_email_domains():
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""select c.full_name ,substr(c.email,(strpos(c.email,'@'))) as domain_name from cw5.customers as c""")
            return cur.fetchall()

# 5- İsim ve email birleştir
def concat_name_and_email():
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""select concat(c.full_name,' - ',c.email) as full_info from cw5.customers as c""")
            return cur.fetchall()

# 6- Sipariş tutarlarını tam sayıya çevir
def cast_total_amount_to_integer():
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""select o.order_id, cast(o.total_amount as integer) as total_amount_int  from cw5.orders as o""")
            return cur.fetchall()

# 7- Email '@' pozisyonu
def find_at_position_in_email():
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""select c.full_name ,POSITION('@' IN c.email) as at_position from cw5.customers as c""")
            return cur.fetchall()

# 8- NULL kategoriye 'Unknown' yaz
def fill_null_product_category():
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""select p.product_name,coalesce(category,'unknown') as product_category from cw5.products  as p  """)
            return cur.fetchall()

# 9- Müşteri harcama sıralaması (RANK)
def rank_customers_by_spending():
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""select o.order_id, o.total_amount, RANK() over (order by o.total_amount desc) as rank_by_spend from cw5.orders as o""")
            return cur.fetchall()

# 10- Müşteri siparişlerinde running total
def running_total_per_customer():
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""select o.order_id,o.customer_id, o.total_amount ,sum(o.total_amount) over (order by o.order_date )as running_total from cw5.orders as o""")
            return cur.fetchall()

# 11- Elektronik ve Beyaz Eşya ürünleri (UNION)
def get_electronics_and_appliances():
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""select p.product_name,p.category from cw5.products as p where p.category='Electronics' UNION select p.product_name,p.category from cw5.products as p where p.category='Appliances'""")
            return cur.fetchall()

# 12- Tüm siparişler ve eksik siparişler (UNION ALL)
def get_orders_with_missing_customers():
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""select o.customer_id, o.total_amount from cw5.orders as o where o.status='completed' UNION select o.customer_id, o.total_amount  from cw5.orders as o where o.status='pending'""")
            return cur.fetchall()