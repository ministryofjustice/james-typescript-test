import sys
import json

sev_lookup={
  'high':'error',
  'moderate':'warning',
  'low':'note'
}

def eprint(*args, **kwargs):
  print(*args, file=sys.stderr, **kwargs)

def main():
  if len(sys.argv)<2:
    eprint('Usage: python3 outdated_to_slack.py <<input.txt>> [-o output.json]')
    sys.exit(1)

  # Default for output file if required
  args=sys.argv
  input_file=args[1]
  output_file=f"{args[1].split('.')[0]}.json"
  for each_arg in args:
    if each_arg=='-o' and len(args)>(args.index('-o')+1):
      output_file=args[args.index('-o')+1]

  slack_template = { 
    "text": "npm outdated scan identified issues",
    "blocks": [
      {
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": ":warning: Github Actions *npm outdated reports check* ran and identified issues"
        }
      },
      {
        "type": "section",
        "fields": [
          {
            "type": "mrkdwn",
            "text": ""
          }
        ]
      },
      {
        "type": "section",
        "fields": [
          {
            "type": "mrkdwn",
            "text": "*Workflow:*\n<${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}|${{ github.workflow }}>"
          },
          {
            "type": "mrkdwn",
            "text": "*Job:*\n${{ github.job }}"
          },
          {
            "type": "mrkdwn",
            "text": "*Repo:*\n${{ github.repository }}"
          },
          {
            "type": "mrkdwn",
            "text": "*Project:*\n${{ github.event.repository.name }}"
          }
        ]
      }
    ]
  }

  results=''
  try:
    with open(input_file) as f:
      results=f.read()
    f.close()     
  except:
    eprint("Encountered an error - please check the input file")
    sys.exit(1)
  if results:
    slack_template['blocks'][2]['fields'][0]['text']=f'```{results}```'


  with open(output_file,'w') as f:
    json.dump(slack_template, f)
  f.close()

if __name__ == '__main__':
  main()