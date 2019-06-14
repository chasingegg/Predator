import csv


class HtmlOutputer(object):
    def __init__(self):
        self.datas = []

    def collect_data(self, new_data):
        if new_data is None:
            return
        self.datas.append(new_data)

    def output_html(self):
        # fout = open('output.html', 'w', encoding='UTF-8')
        # fout.write('<html>')
        # fout.write('<head><meta charset="utf-8"></head>')
        # fout.write('<body>')
        # fout.write('<table>')
        # #
        path = "./baike.csv"
        out = open(path, 'a', newline='')
        csv_write = csv.writer(out, dialect='excel')

        for data in self.datas:
            # fout.write('<tr>')
            # fout.write("<td>%s</td>" % data['url'])
            row = []
            title = str(data['title']).replace('\n', '').replace('\r', '')
            # title = str(data['title']).replace('/r', '')
            summary = str(data['summary']).replace('\n', '').replace('\r', '')
            # summary = str(data['summary']).replace('/r', '')
            # print(data['title'])
            # print(summary)
            row.append(title)
            row.append(summary)
            csv_write.writerow(row)
            # fout.write("<td>%s</td>" % data['title'])
            # fout.write("<td>%s</td>" % data['summary'])
            # fout.write('</tr>')
        # fout.write('</table>')
        # fout.write('</body>')
        # fout.write('</html>')

        # fout.close()
