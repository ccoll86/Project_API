#--------------CLI--------------#
@app.route('/CLI/<int:n>')

def read():
   product_list_url = 'http://localhost:5000/'
   response = requests.get(product_list_url)

   return response.json()

def save(data):
    with open('product_data.csv', 'w') as f:
        field_names = ['id', 'name', 'product_id', 'description']
    writer = csv.DictWriter(f, fieldnames=field_names)

    writer.writeheader()
    for row in data.json():
        writer.writerow(row)


if __name__ == '__main__':
   parser = ArgumentParser(description='A command line tool for interacting with our API')
   parser.add_argument('-r', '--read', action='store_true', help='Sends a GET request to the product API.')
   parser.add_argument('-p', '--preview', action='store_true', help='Shows us a preview of the data.')
   parser.add_argument('-s', '--save', action='store_true', help='Save the response.')
   args = parser.parse_args()

   if args.read:
       read()
   if args.preview:
       preview(read())
   else:
       print('Use the -h or --help flags for help')

