from fpdf import FPDF

def create_table(table_data, sum_up='',title='', data_size = 10,
    title_style='B', title_size=12, align_data='L', 
    align_header='L', cell_width='even', x_start='x_default',
    emphasize_data=[], emphasize_style=None, emphasize_color=(0,0,0), show_header=True):
    """
    table_data: 
                list of lists with first element being list of headers
    title: 
                (Optional) title of table (optional)
    data_size: 
                the font size of table data
    title_size: 
                the font size fo the title of the table
    align_data: 
                align table data
                L = left align
                C = center align
                R = right align
    align_header: 
                align table data
                L = left align
                C = center align
                R = right align
    cell_width: 
                even: evenly distribute cell/column width
                uneven: base cell size on lenght of cell/column items
                int: int value for width of each cell/column
                list of ints: list equal to number of columns with the widht of each cell / column
    x_start: 
                where the left edge of table should start
    emphasize_data:  
                which data elements are to be emphasized - pass as list 
                emphasize_style: the font style you want emphaized data to take
                emphasize_color: emphasize color (if other than black) 
    
    """
    default_style = pdf.font_style
    if emphasize_style == None:
        emphasize_style = default_style
    # default_font = pdf.font_family
    # default_size = pdf.font_size_pt
    # default_style = pdf.font_style
    # default_color = pdf.color # This does not work

    # Get Width of Columns
    def get_col_widths():
        col_width = cell_width
        if col_width == 'even':
            col_width = pdf.epw / len(data[0]) - 1  # distribute content evenly   # epw = effective page width (width of page not including margins)
        elif col_width == 'uneven':
            col_widths = []

            # searching through columns for largest sized cell (not rows but cols)
            for col in range(len(table_data[0])): # for every row
                longest = 0 
                for row in range(len(table_data)):
                    cell_value = str(table_data[row][col])
                    value_length = pdf.get_string_width(cell_value)
                    if value_length > longest:
                        longest = value_length
                col_widths.append(longest + 4) # add 4 for padding
            col_width = col_widths



                    ### compare columns 

        elif isinstance(cell_width, list):
            col_width = cell_width  # TODO: convert all items in list to int        
        else:
            # TODO: Add try catch
            col_width = int(col_width)
        return col_width

    # Convert dict to lol
    # Why? because i built it with lol first and added dict func after
    # Is there performance differences?
    if isinstance(table_data, dict):
        header = [key for key in table_data]
        data = []
        for key in table_data:
            value = table_data[key]
            data.append(value)
        # need to zip so data is in correct format (first, second, third --> not first, first, first)
        data = [list(a) for a in zip(*data)]

    else:
        header = table_data[0]
        data = table_data[1:]

    line_height = pdf.font_size * 2.5

    col_width = get_col_widths()
    pdf.set_font(size=title_size, style=title_style)

    # Get starting position of x
    # Determin width of table to get x starting point for centred table
    if x_start == 'C':
        table_width = 0
        if isinstance(col_width, list):
            for width in col_width:
                table_width += width
        else: # need to multiply cell width by number of cells to get table width 
            table_width = col_width * len(table_data[0])
        # Get x start by subtracting table width from pdf width and divide by 2 (margins)
        margin_width = pdf.w - table_width
        # TODO: Check if table_width is larger than pdf width

        center_table = margin_width / 2 # only want width of left margin not both
        x_start = center_table
        pdf.set_x(x_start)
    elif isinstance(x_start, int):
        pdf.set_x(x_start)
    elif x_start == 'x_default':
        x_start = pdf.set_x(pdf.l_margin)


    # TABLE CREATION #

    # add title
    if title != '':
        pdf.multi_cell(0, line_height, title, border=0, align='j', ln=3, max_line_height=pdf.font_size)
        pdf.ln(line_height) # move cursor back to the left margin

    pdf.set_font(size=data_size)
    # add header
    y1 = pdf.get_y()
    if x_start:
        x_left = x_start
    else:
        x_left = pdf.get_x()
    x_right = pdf.epw + x_left
    if  not isinstance(col_width, list):
        if x_start:
            pdf.set_x(x_start)
        if show_header:
            for datum in header:
                pdf.multi_cell(col_width, line_height, datum, border=0, align=align_header, ln=3, max_line_height=pdf.font_size)
                x_right = pdf.get_x()
            pdf.ln(line_height) # move cursor back to the left margin
            y2 = pdf.get_y()
            pdf.line(x_left,y1,x_right,y1)
            pdf.line(x_left,y2,x_right,y2)

        for row in data:
            if x_start: # not sure if I need this
                pdf.set_x(x_start)
            for datum in row:
                if datum in emphasize_data:
                    pdf.set_text_color(*emphasize_color)
                    pdf.set_font(style=emphasize_style)
                    pdf.multi_cell(col_width, line_height, datum, border=0, align=align_data, ln=3, max_line_height=pdf.font_size)
                    pdf.set_text_color(0,0,0)
                    pdf.set_font(style=default_style)
                else:
                    pdf.multi_cell(col_width, line_height, datum, border=0, align=align_data, ln=3, max_line_height=pdf.font_size) # ln = 3 - move cursor to right with same vertical offset # this uses an object named pdf
            pdf.ln(line_height) # move cursor back to the left margin
    
    else:
        if x_start:
            pdf.set_x(x_start)
        if show_header:
            for i in range(len(header)):
                datum = header[i]
                pdf.multi_cell(col_width[i], line_height, datum, border=0, align=align_header, ln=3, max_line_height=pdf.font_size)
                x_right = pdf.get_x()
            pdf.ln(line_height) # move cursor back to the left margin
            y2 = pdf.get_y()
            pdf.line(x_left,y1,x_right,y1)
            pdf.line(x_left,y2,x_right,y2)


        for i in range(len(data)):
            if x_start:
                pdf.set_x(x_start)
            row = data[i]
            for i in range(len(row)):
                datum = row[i]
                if not isinstance(datum, str):
                    datum = str(datum)
                adjusted_col_width = col_width[i]
                if datum in emphasize_data:
                    pdf.set_text_color(*emphasize_color)
                    pdf.set_font(style=emphasize_style)
                    pdf.multi_cell(adjusted_col_width, line_height, datum, border=0, align=align_data, ln=3, max_line_height=pdf.font_size)
                    pdf.set_text_color(0,0,0)
                    pdf.set_font(style=default_style)
                else:
                    pdf.multi_cell(adjusted_col_width, line_height, datum, border=0, align=align_data, ln=3, max_line_height=pdf.font_size) # ln = 3 - move cursor to right with same vertical offset # this uses an object named pdf
            pdf.ln(line_height) # move cursor back to the left margin
    y3 = pdf.get_y()
    if show_header:
        pdf.line(x_left,y3,x_right,y3)

    if sum_up != '':
        pdf.set_font(style='B')
        pdf.multi_cell(0, line_height, sum_up, border=0, align='j', ln=3, max_line_height=pdf.font_size)
        pdf.ln(line_height) # move cursor back to the left margin    




pdf = FPDF()
pdf.add_page()
pdf.set_font('Times', size=10)

pdf.cell(txt='A/C No:test Name: test test')
pdf.ln()

transactions = (
    ("Ticket", "Open Time", "TypeSize", "Item", "Open", "Price", "S/LT/PClose", "TimeClose","PriceCommissionSwapTrade"),
    ("test", "test", "test", "test", "test", "test", "test", "test","test"),
    ("test", "test", "test", "test", "test", "test", "test", "test","test"),
    ("test", "test", "test", "test", "test", "test", "test", "test","test"),
    ("test", "test", "test", "test", "test", "test", "test", "test","test"),
    ("test", "test", "test", "test", "test", "test", "test", "test","test"),
)
working_orders = (
    ("TicketOpen", "TimeType", "Size", "Item", "Price", "S/LT/P"),
    ("test", "test", "test", "tes", "tes", "test"),
    ("test", "test", "test", "tes", "tes", "test"),
    ("test", "test", "test", "tes", "tes", "test"),
    ("test", "test", "test", "tes", "tes", "test"),
)

summary = (
    ("Previous Ledger Balance", "test", "Floating P/L:", "test"),
    ("Close Trade P/L", "test", "Total Credit Facility:", "test"),
    ("Deposit/Withdrawal:", "test", "Equity:", "test"),
    ("Balance:", "test", "Mergin Requirements:", "test"),
    ("", "", "Mergin Requirements:", "test"),
)

create_table(table_data = transactions, sum_up='test test Close Trade P/L: test', title='Closed Transactions:', cell_width='uneven', title_size=18)
pdf.ln()
create_table(table_data = working_orders, sum_up='A/C Summary', title='Working Orders:', cell_width='uneven', title_size=20)
pdf.ln()
create_table(table_data = summary, sum_up='', title='', cell_width='uneven', show_header=False)
pdf.ln()

pdf.set_font(size=36, style='b')
pdf.cell(txt='Best Regards')
pdf.ln()
pdf.cell(txt='Accounts Department')
pdf.ln()
pdf.set_font(size=20)
pdf.cell(txt='Please report to us within 24 hours if this statement is', center=True)
pdf.ln()
pdf.cell(txt='incorect. Otherwise this statement will be considered', center=True)
pdf.ln()
pdf.cell(txt='be confirm by', center=True)

pdf.output('text.pdf')