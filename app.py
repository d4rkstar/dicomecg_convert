#!flask/bin/python
from __future__ import unicode_literals, print_function, division, absolute_import
from flask import Flask
from flask import request
from flask import jsonify


from future import standard_library
standard_library.install_aliases()
from ecg import ECG
from docopt import docopt
import io

app = Flask(__name__)


def convert(source, layout, outformat, outputfile,
            minor_axis=False, interpretation=False):

    ecg = ECG(source)
    ecg.draw(layout, 10, minor_axis, interpretation=interpretation)
    return ecg.save(outformat=outformat, outputfile=outputfile)


@app.route('/dicom', methods=['POST'])
def post():
    try:
        content = request.get_json()
        byte_content = content['input']

        base64_string = byte_content.decode('base64')

        if 'format' in content:
            outformat = content['format']
        else:
            outformat = None

        if 'layout' in content:
            layout = content['layout']
        else:
            layout = None

        if 'minor-grid' in content:
            minor_axis = content['minor-grid']
        else:
            minor_axis = False

        interpretation = True

        source = io.BytesIO(bytes(base64_string))

        output = convert(source, layout, outformat, None, minor_axis, interpretation)

        return jsonify(
            error=None,
            format=outformat,
            output=output.encode('base64')
        )
    except Exception, e:
        return jsonify(
            error='Failed to operate conversion: ' + str(e)
        )


app.run(host='0.0.0.0', port=5000)