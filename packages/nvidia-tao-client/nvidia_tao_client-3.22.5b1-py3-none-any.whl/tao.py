# SPDX-FileCopyrightText: Copyright (c) 2022 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

import os
import click
import requests
import json
import enum

@click.group()
@click.version_option(package_name='nvidia-tao-client')
@click.pass_context
def cli(ctx):
    pass

#
# SPECTRO_GEN
#

@cli.group()
def spectro_gen():
    pass

class spectro_gen_dataset_format(str, enum.Enum):
    ljspeech = "ljspeech"
    custom = "custom"

@spectro_gen.command()
@click.option('--format', prompt='format', type=click.Choice(spectro_gen_dataset_format), help='The dataset format.', required=True)
def dataset_create(format):
    base_url = os.getenv('BASE_URL')
    data = json.dumps( {"type": "speech", "format": format} )
    endpoint = base_url + "/dataset"
    response = requests.post(endpoint, data=data)
    id = response.json()["id"]
    click.echo(f"{id}")

@spectro_gen.command()
@click.option('--id', prompt='id', help='The dataset ID.', required=True)
def dataset_convert_defaults(id):
    base_url = os.getenv('BASE_URL')
    endpoint = base_url + "/dataset/{}/specs/{}/schema".format(id, "convert")
    response = requests.get(endpoint)
    data = response.json()["default"]
    click.echo(json.dumps(data, indent=2))

@spectro_gen.command()
@click.option('--id', prompt='id', help='The dataset ID.', required=True)
def dataset_convert(id):
    base_url = os.getenv('BASE_URL')
    data = json.dumps( { "job": None, "actions": ["convert"] } )
    endpoint = base_url + "/dataset/" + id + "/job"
    response = requests.post(endpoint, data=data)
    job_id = response.json()[0]
    click.echo(f"{job_id}")

@spectro_gen.command()
def model_create():
    base_url = os.getenv('BASE_URL')
    data = json.dumps( {"network_arch": "spectro_gen", "encryption_key": "tlt_encode"} )
    endpoint = base_url + "/model"
    response = requests.post(endpoint, data=data)
    id = response.json()["id"]
    click.echo(f"{id}")

@spectro_gen.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
def model_dataset_convert_defaults(id):
    base_url = os.getenv('BASE_URL')
    endpoint = base_url + "/model/{}/specs/{}/schema".format(id, "dataset_convert")
    response = requests.get(endpoint)
    data = response.json()["default"]
    click.echo(json.dumps(data, indent=2))

@spectro_gen.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
def model_dataset_convert(id):
    base_url = os.getenv('BASE_URL')
    data = json.dumps( { "job": None, "actions": ["dataset_convert"] } )
    endpoint = base_url + "/model/" + id + "/job"
    response = requests.post(endpoint, data=data)
    job_id = response.json()[0]
    click.echo(f"{job_id}")

@spectro_gen.command()
@click.option('--id', prompt='id', help='The dataset ID.', required=True)
def dataset_pitch_stats_defaults(id):
    base_url = os.getenv('BASE_URL')
    endpoint = base_url + "/dataset/{}/specs/{}/schema".format(id, "pitch_stats")
    response = requests.get(endpoint)
    data = response.json()["default"]
    click.echo(json.dumps(data, indent=2))

@spectro_gen.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
@click.option('--job', prompt='job', help='The job ID.', required=True)
def dataset_job_cancel(id, job):
    base_url = os.getenv('BASE_URL')
    endpoint = base_url + "/dataset/" + id + "/job/" + job + "/cancel"
    response = requests.post(endpoint)
    click.echo(f"{job}")

@spectro_gen.command()
@click.option('--id', prompt='id', help='The dataset ID.', required=True)
@click.option('--job', help='The dataset convert job ID.', required=False, default=None)
def dataset_pitch_stats(id, job):
    base_url = os.getenv('BASE_URL')
    data = json.dumps( {"job": job, "actions": ["pitch_stats"] } )
    endpoint = base_url + "/dataset/" + id + "/job"
    response = requests.post(endpoint, data=data)
    job_id = response.json()[0]
    click.echo(f"{job_id}")

@spectro_gen.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
def model_finetune_defaults(id):
    base_url = os.getenv('BASE_URL')
    endpoint = base_url + "/model/{}/specs/{}/schema".format(id, "finetune")
    response = requests.get(endpoint)
    data = response.json()["default"]
    click.echo(json.dumps(data, indent=2))

@spectro_gen.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
@click.option('--job', help='The pitch stats job ID.', required=False, default=None)
def model_finetune(id, job):
    base_url = os.getenv('BASE_URL')
    data = json.dumps( {"job": job, "actions": ["finetune"]} )
    endpoint = base_url + "/model/" + id + "/job"
    response = requests.post(endpoint, data=data)
    job_id = response.json()[0]
    click.echo(f"{job_id}")

@spectro_gen.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
def model_infer_defaults(id):
    base_url = os.getenv('BASE_URL')
    endpoint = base_url + "/model/{}/specs/{}/schema".format(id, "infer")
    response = requests.get(endpoint)
    data = response.json()["default"]
    click.echo(json.dumps(data, indent=2))

@spectro_gen.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
@click.option('--job', help='The finetune job ID.', required=False, default=None)
def model_infer(id, job):
    base_url = os.getenv('BASE_URL')
    data = json.dumps( {"job": job, "actions": ["infer"]} )
    endpoint = base_url + "/model/" + id + "/job"
    response = requests.post(endpoint, data=data)
    job_id = response.json()[0]
    click.echo(f"{job_id}")

@spectro_gen.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
@click.option('--job', prompt='job', help='The job ID.', required=True)
def model_job_cancel(id, job):
    base_url = os.getenv('BASE_URL')
    endpoint = base_url + "/model/" + id + "/job/" + job + "/cancel"
    response = requests.post(endpoint)
    click.echo(f"{job}")

@spectro_gen.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
@click.option('--job', prompt='job', help='The job ID.', required=True)
def model_job_resume(id, job):
    base_url = os.getenv('BASE_URL')
    endpoint = base_url + "/model/" + id + "/job/" + job + "/resume"
    response = requests.post(endpoint)
    click.echo(f"{job}")


#
# VOCODER
#

@cli.group()
def vocoder():
    pass

class vocoder_dataset_format(str, enum.Enum):
    hifigan = "hifigan"
    raw = "raw"

@vocoder.command()
@click.option('--format', prompt='format', type=click.Choice(vocoder_dataset_format), help='The dataset format.', required=True)
def dataset_create(format):
    base_url = os.getenv('BASE_URL')
    data = json.dumps( {"type": "mel_spectrogram", "format": format} )
    endpoint = base_url + "/dataset"
    response = requests.post(endpoint, data=data)
    id = response.json()["id"]
    click.echo(f"{id}")

@vocoder.command()
def model_create():
    base_url = os.getenv('BASE_URL')
    data = json.dumps( {"network_arch": "vocoder", "encryption_key": "tlt_encode"} )
    endpoint = base_url + "/model"
    response = requests.post(endpoint, data=data)
    id = response.json()["id"]
    click.echo(f"{id}")

@vocoder.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
def model_finetune_defaults(id):
    base_url = os.getenv('BASE_URL')
    endpoint = base_url + "/model/{}/specs/{}/schema".format(id, "finetune")
    response = requests.get(endpoint)
    data = response.json()["default"]
    click.echo(json.dumps(data, indent=2))

@vocoder.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
@click.option('--job', help='The spectro_gen infer job ID.', required=False, default=None)
def model_finetune(id, job):
    base_url = os.getenv('BASE_URL')
    data = json.dumps( {"job": job, "actions": ["finetune"]} )
    endpoint = base_url + "/model/" + id + "/job"
    response = requests.post(endpoint, data=data)
    job_id = response.json()[0]
    click.echo(f"{job_id}")

@vocoder.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
def model_infer_defaults(id):
    base_url = os.getenv('BASE_URL')
    endpoint = base_url + "/model/{}/specs/{}/schema".format(id, "infer")
    response = requests.get(endpoint)
    data = response.json()["default"]
    click.echo(json.dumps(data, indent=2))

@vocoder.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
@click.option('--job', help='The finetune job ID.', required=False, default=None)
def model_infer(id, job):
    base_url = os.getenv('BASE_URL')
    data = json.dumps( {"job": job, "actions": ["infer"]} )
    endpoint = base_url + "/model/" + id + "/job"
    response = requests.post(endpoint, data=data)
    job_id = response.json()[0]
    click.echo(f"{job_id}")

@vocoder.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
@click.option('--job', prompt='job', help='The job ID.', required=True)
def model_job_cancel(id, job):
    base_url = os.getenv('BASE_URL')
    endpoint = base_url + "/model/" + id + "/job/" + job + "/cancel"
    response = requests.post(endpoint)
    click.echo(f"{job}")

@vocoder.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
@click.option('--job', prompt='job', help='The job ID.', required=True)
def model_job_resume(id, job):
    base_url = os.getenv('BASE_URL')
    endpoint = base_url + "/model/" + id + "/job/" + job + "/resume"
    response = requests.post(endpoint)
    click.echo(f"{job}")


#
# DETECTNET_V2
#

@cli.group()
def detectnet_v2():
    pass

class detectnet_v2_dataset_format(str, enum.Enum):
    kitti = "kitti"
    coco = "coco"
    raw = "raw"

@detectnet_v2.command()
@click.option('--format', prompt='format', type=click.Choice(detectnet_v2_dataset_format), help='The dataset format.', required=True)
def dataset_create(format):
    base_url = os.getenv('BASE_URL')
    data = json.dumps( {"type": "object_detection", "format": format} )
    endpoint = base_url + "/dataset"
    response = requests.post(endpoint, data=data)
    id = response.json()["id"]
    click.echo(f"{id}")

@detectnet_v2.command()
def model_create():
    base_url = os.getenv('BASE_URL')
    data = json.dumps( {"network_arch": "detectnet_v2", "encryption_key": "tlt_encode"} )
    endpoint = base_url + "/model"
    response = requests.post(endpoint, data=data)
    id = response.json()["id"]
    click.echo(f"{id}")

@detectnet_v2.command()
@click.option('--id', prompt='id', help='The dataset ID.', required=True)
def dataset_convert_defaults(id):
    base_url = os.getenv('BASE_URL')
    endpoint = base_url + "/dataset/{}/specs/{}/schema".format(id, "convert")
    response = requests.get(endpoint)
    data = response.json()["default"]
    click.echo(json.dumps(data, indent=2))

@detectnet_v2.command()
@click.option('--id', prompt='id', help='The dataset ID.', required=True)
def dataset_convert(id):
    base_url = os.getenv('BASE_URL')
    data = json.dumps( { "job": None, "actions": ["convert"] } )
    endpoint = base_url + "/dataset/" + id + "/job"
    response = requests.post(endpoint, data=data)
    job_id = response.json()[0]
    click.echo(f"{job_id}")

@detectnet_v2.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
@click.option('--job', prompt='job', help='The job ID.', required=True)
def dataset_job_cancel(id, job):
    base_url = os.getenv('BASE_URL')
    endpoint = base_url + "/dataset/" + id + "/job/" + job + "/cancel"
    response = requests.post(endpoint)
    click.echo(f"{job}")

@detectnet_v2.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
def model_train_defaults(id):
    base_url = os.getenv('BASE_URL')
    endpoint = base_url + "/model/{}/specs/{}/schema".format(id, "train")
    response = requests.get(endpoint)
    data = response.json()["default"]
    click.echo(json.dumps(data, indent=2))

@detectnet_v2.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
@click.option('--job', help='The dataset convert job ID.', required=False, default=None)
def model_train(id, job):
    base_url = os.getenv('BASE_URL')
    data = json.dumps( { "job": job, "actions": ["train"] } )
    endpoint = base_url + "/model/" + id + "/job"
    response = requests.post(endpoint, data=data)
    job_id = response.json()[0]
    click.echo(f"{job_id}")

@detectnet_v2.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
def model_evaluate_defaults(id):
    base_url = os.getenv('BASE_URL')
    endpoint = base_url + "/model/{}/specs/{}/schema".format(id, "evaluate")
    response = requests.get(endpoint)
    data = response.json()["default"]
    click.echo(json.dumps(data, indent=2))

@detectnet_v2.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
@click.option('--job', help='The train, prune or retrain job ID.', required=False, default=None)
def model_evaluate(id, job):
    base_url = os.getenv('BASE_URL')
    data = json.dumps( { "job": job, "actions": ["evaluate"] } )
    endpoint = base_url + "/model/" + id + "/job"
    response = requests.post(endpoint, data=data)
    job_id = response.json()[0]
    click.echo(f"{job_id}")

@detectnet_v2.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
def model_export_defaults(id):
    base_url = os.getenv('BASE_URL')
    endpoint = base_url + "/model/{}/specs/{}/schema".format(id, "export")
    response = requests.get(endpoint)
    data = response.json()["default"]
    click.echo(json.dumps(data, indent=2))

@detectnet_v2.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
@click.option('--job', help='The train, prune or retrain job ID.', required=False, default=None)
def model_export(id, job):
    base_url = os.getenv('BASE_URL')
    data = json.dumps( { "job": job, "actions": ["export"] } )
    endpoint = base_url + "/model/" + id + "/job"
    response = requests.post(endpoint, data=data)
    job_id = response.json()[0]
    click.echo(f"{job_id}")

@detectnet_v2.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
def model_convert_defaults(id):
    base_url = os.getenv('BASE_URL')
    endpoint = base_url + "/model/{}/specs/{}/schema".format(id, "convert")
    response = requests.get(endpoint)
    data = response.json()["default"]
    click.echo(json.dumps(data, indent=2))

@detectnet_v2.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
@click.option('--job', help='The export job ID.', required=False, default=None)
def model_convert(id, job):
    base_url = os.getenv('BASE_URL')
    data = json.dumps( { "job": job, "actions": ["convert"] } )
    endpoint = base_url + "/model/" + id + "/job"
    response = requests.post(endpoint, data=data)
    job_id = response.json()[0]
    click.echo(f"{job_id}")

@detectnet_v2.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
def model_inference_defaults(id):
    base_url = os.getenv('BASE_URL')
    endpoint = base_url + "/model/{}/specs/{}/schema".format(id, "inference")
    response = requests.get(endpoint)
    data = response.json()["default"]
    click.echo(json.dumps(data, indent=2))

@detectnet_v2.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
@click.option('--job', help='The train, prune, retrain, export or convert job ID.', required=False, default=None)
def model_inference(id, job):
    base_url = os.getenv('BASE_URL')
    data = json.dumps( { "job": job, "actions": ["inference"] } )
    endpoint = base_url + "/model/" + id + "/job"
    response = requests.post(endpoint, data=data)
    job_id = response.json()[0]
    click.echo(f"{job_id}")

@detectnet_v2.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
def model_prune_defaults(id):
    base_url = os.getenv('BASE_URL')
    endpoint = base_url + "/model/{}/specs/{}/schema".format(id, "prune")
    response = requests.get(endpoint)
    data = response.json()["default"]
    click.echo(json.dumps(data, indent=2))

@detectnet_v2.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
@click.option('--job', help='The train job ID.', required=False, default=None)
def model_prune(id, job):
    base_url = os.getenv('BASE_URL')
    data = json.dumps( { "job": job, "actions": ["prune"] } )
    endpoint = base_url + "/model/" + id + "/job"
    response = requests.post(endpoint, data=data)
    job_id = response.json()[0]
    click.echo(f"{job_id}")

@detectnet_v2.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
def model_retrain_defaults(id):
    base_url = os.getenv('BASE_URL')
    endpoint = base_url + "/model/{}/specs/{}/schema".format(id, "retrain")
    response = requests.get(endpoint)
    data = response.json()["default"]
    click.echo(json.dumps(data, indent=2))

@detectnet_v2.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
@click.option('--job', help='The prune job ID.', required=False, default=None)
def model_retrain(id, job):
    base_url = os.getenv('BASE_URL')
    data = json.dumps( { "job": job, "actions": ["retrain"] } )
    endpoint = base_url + "/model/" + id + "/job"
    response = requests.post(endpoint, data=data)
    job_id = response.json()[0]
    click.echo(f"{job_id}")

@detectnet_v2.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
@click.option('--job', prompt='job', help='The job ID.', required=True)
def model_job_cancel(id, job):
    base_url = os.getenv('BASE_URL')
    endpoint = base_url + "/model/" + id + "/job/" + job + "/cancel"
    response = requests.post(endpoint)
    click.echo(f"{job}")

@detectnet_v2.command()
@click.option('--id', prompt='id', help='The model ID.', required=True)
@click.option('--job', prompt='job', help='The job ID.', required=True)
def model_job_resume(id, job):
    base_url = os.getenv('BASE_URL')
    endpoint = base_url + "/model/" + id + "/job/" + job + "/resume"
    response = requests.post(endpoint)
    click.echo(f"{job}")


if __name__ == '__main__':
    cli()

