# Api specific functions
import connexion
from connexion import problem
from werkzeug.utils import secure_filename
from flask import send_file
import logging
import os

from pychubby import cli
import matplotlib.pyplot as plt
import pychubby.actions
from pychubby.detect import LandmarkFace

ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg"])

logger = logging.getLogger("phchubby-api")


def get_actions():
    actions = cli.ALL_ACTIONS
    result = {"actions": actions}
    return result, 200


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def perform(*args, **kwargs):
    """Perform an action."""

    action = kwargs.get("action", None)
    logger.info("action: {} START".format(action))
    # Get uploaded file information:
    file = connexion.request.files["inp_img"]

    if action not in cli.ALL_ACTIONS:
        return problem(
            title="Wrong Action",
            detail="The action: {} does not exist.".format(action),
            status=400,
        )

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join("/tmp/", filename))

        logger.info("inp_file: {}".format(file.filename))
        img = plt.imread("/tmp/{}".format(filename))

        logger.info("LandmarkFace.estimate")
        lf = LandmarkFace.estimate(img)
        logger.info("pychubby action: {}".format(action))
        cls = getattr(pychubby.actions, action)
        a = pychubby.actions.Multiple(cls())

        logger .info("new_lf: a.perform")
        new_lf, df = a.perform(lf)
        out_img = "/tmp/chubbyfied_{}".format(file.filename)
        logger.info("Saving output image: {}".format(out_img))
        plt.imsave(str(out_img), new_lf[0].img)

        logger.info("action: {} END".format(action))
        return send_file(out_img), 200
    else:
        return problem(
            title="File not allowed",
            detail="The Input File: '{}' is not allowed.".format(file.filename),
            status=400,
        )
