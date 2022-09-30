# calculator
# Built with Seahorse v0.1.0
#
# Gives users their own on-chain four-function calculator!

from seahorse.prelude import *

declare_id('Fg6PaFpoGXkYsidMpWTK6W2BeZ7FEfcYkg476zPFsLnS')

class Calculator(Account):
  owner: Pubkey
  display: i64

class Operation(Enum):
  ADD = 0
  SUB = 1
  MUL = 2
  DIV = 3

@instruction
def init_calculator(owner: Signer, calculator: Empty[Calculator]):
  calculator = calculator.init(payer = owner, seeds = ['Calculator', owner])
  calculator.owner = owner.key()

@instruction
def reset_calculator(owner: Signer, calculator: Calculator):
  print(owner.key(), 'is resetting a calculator', calculator.key())

  assert owner.key() == calculator.owner, 'This is not your calculator!'

  calculator.display = 0

@instruction
def do_operation(owner: Signer, calculator: Calculator, op: Operation, num: i64):
  assert owner.key() == calculator.owner, 'This is not your calculator!'

  if op == Operation.ADD:
    calculator.display += num
  elif op == Operation.SUB:
    calculator.display -= num
  elif op == Operation.MUL:
    calculator.display *= num
  elif op == Operation.DIV:
    calculator.display /= num

@instruction
def use_token_mint(
  mint: TokenMint,
  recipient: TokenAccount,
  signer: Signer,
  recipient_signer: Signer
):
  # Mint 100 tokens from our `mint` to `recipient`.
  # `signer` must be the authority (owner) for `mint`.
  # Note that the amounts here are in *native* token quantities - you need to
  # account for decimals when you make calls to .mint().
  mint.mint(
    authority = signer,
    to = recipient,
    amount = 100
  )
  
  # Burn 99 tokens from the `recipient` account (so after this instruction,
  # `recipient` will gain exactly 1 token.)
  # `recipient_signer` must be the authority for the `recipient` token account.
  mint.burn(
    authority = recipient_signer,
    to = recipient,
    amount = 99
  )
